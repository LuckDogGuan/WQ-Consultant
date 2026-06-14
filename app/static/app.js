/* WQ Consultant GUI Client Javascript Code */

// 全局轮询定时器
let jobsInterval = null;
let detailLogInterval = null;
let detailEventsInterval = null;
let guiLogInterval = null;

let currentSelectedJobId = null;
let currentDetailsTab = 'log'; // 'log' or 'events'

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 启动页面初始挂载
document.addEventListener("DOMContentLoaded", function() {
    restoreMobileMenuScroll();
    // 开启网络状态监测轮询
    checkNetworkStatus();
    setInterval(checkNetworkStatus, 4000);

    // 如果存在 jobs-table，则开启定时轮询任务状态
    if (document.getElementById("jobs-table") || document.getElementById("backtest-jobs-table")) {
        startJobsPolling();
    }
});

function restoreMobileMenuScroll() {
    const menu = document.querySelector(".sidebar-menu");
    if (!menu) return;

    const savedLeft = sessionStorage.getItem("sidebar_menu_scroll_left");
    if (savedLeft !== null) {
        menu.scrollLeft = parseInt(savedLeft, 10) || 0;
    }

    menu.addEventListener("scroll", () => {
        sessionStorage.setItem("sidebar_menu_scroll_left", String(menu.scrollLeft));
    }, { passive: true });

    menu.addEventListener("click", () => {
        sessionStorage.setItem("sidebar_menu_scroll_left", String(menu.scrollLeft));
    });
}

// ==========================================
// 任务管理与操作 API
// ==========================================

function startJobsPolling() {
    updateJobsState();
    jobsInterval = setInterval(updateJobsState, 4000); // 每 4 秒轮询一次
}

function checkNetworkStatus() {
    fetch("/api/network_status")
        .then(response => response.json())
        .then(data => {
            const indicator = document.getElementById("system-status-indicator");
            const textEl = document.getElementById("system-status-text");
            if (indicator && textEl) {
                if (data.connected) {
                    indicator.classList.remove("disconnected");
                    textEl.innerText = "系统状态正常";
                } else {
                    indicator.classList.add("disconnected");
                    textEl.innerText = data.message || "网络连接已断开 (10分钟重连中...)";
                }
            }
        })
        .catch(err => {
            const indicator = document.getElementById("system-status-indicator");
            const textEl = document.getElementById("system-status-text");
            if (indicator && textEl) {
                indicator.classList.add("disconnected");
                textEl.innerText = "网络异常 (API 连接失败)";
            }
        });
}

function updateJobsState() {
    fetch("/api/jobs")
        .then(response => response.json())
        .then(data => {
            data.forEach(job => {
                // 更新仪表盘或回测历史列表中的行内容
                const row = document.querySelector(`tr[data-job-id="${job.id}"]`) || document.getElementById(`job-tr-${job.id}`);
                if (row) {
                    // 1. 更新状态 Badge
                    const statusTd = row.querySelector(".job-status-cell") || row.cells[2] || row.cells[1];
                    if (statusTd) {
                        statusTd.innerHTML = `<span class="job-status-badge status-${job.status}">${job.status}</span>`;
                    }
                    
                    // 2. 更新说明和参数
                    const titleTd = row.querySelector(".job-title-cell") || (row.cells.length > 5 ? row.cells[3] : null);
                    if (titleTd) {
                        let paramsText = "";
                        if (job.params) {
                            try {
                                const p = JSON.parse(job.params);
                                if (job.kind === 'catalog_refresh') {
                                    paramsText = `地区: ${p.region || '默认'} | 股票池: ${p.universe || '默认'} | 延时: ${p.delay || '默认'}`;
                                } else if (job.kind === 'backtest') {
                                    paramsText = `一阶: ${p.run_fo ? '是' : '否'} | 二阶: ${p.run_so ? '是' : '否'} | 三阶: ${p.run_th ? '是' : '否'}`;
                                    if (p.dataset_ids && p.dataset_ids.length > 0) {
                                        paramsText += ` | 数据集: ${p.dataset_ids.slice(0, 3).join(', ')}${p.dataset_ids.length > 3 ? '...' : ''}`;
                                    }
                                } else if (job.kind === 'check_submission') {
                                    paramsText = p.manual_ids && p.manual_ids.length > 0 ? `手动追加: ${p.manual_ids.slice(0, 3).join(', ')}${p.manual_ids.length > 3 ? '...' : ''}` : '自动合并检查';
                                } else if (job.kind === 'optimization_run') {
                                    paramsText = `来源: ${p.source_mode || 'recent'} | 候选: ${p.candidate_limit || 20} | 每次提交: ${p.children_per_request || 1}`;
                                }
                            } catch(e) {}
                        }
                        titleTd.innerHTML = `
                            <div class="font-bold">${job.title}</div>
                            ${paramsText ? `<div class="job-params-display text-muted" style="margin-top: 4px; font-size: 11px;"><i class="fa-solid fa-sliders"></i> ${paramsText}</div>` : ''}
                        `;
                    }
                    
                    // 3. 更新进度条 (显示个数)
                    const progressTd = row.querySelector(".job-progress-cell") || (row.cells.length > 5 ? row.cells[4] : row.cells[2]);
                    if (progressTd) {
                        const cur = job.progress_current || 0;
                        const tot = job.progress_total || 0;
                        const pct = tot > 0 ? Math.round((cur / tot) * 100) : 0;
                        
                        let progressText = "准备中";
                        if (tot > 0) {
                            progressText = `Pool ${cur} / ${tot} (${pct}%)`;
                        }
                        
                        progressTd.innerHTML = `
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: ${pct}%"></div>
                                <span class="progress-bar-text">${progressText}</span>
                            </div>
                            ${job.message ? `<div class="job-progress-detail">${escapeHtml(job.message)}</div>` : ''}
                        `;
                    }

                    // 4. 更新消息说明 (如果有关联的 cell)
                    const messageTd = row.querySelector(".job-message-cell");
                    if (messageTd) {
                        messageTd.innerText = job.message || '—';
                    }
                    
                    // 5. 更新操作按钮
                    const actionTd = row.querySelector(".job-action-cell");
                    if (actionTd) {
                        let btnHtml = '<div class="btn-group">';
                        if (['running', 'waiting_limit', 'waiting_time_window', 'reconnecting', 'waiting_network'].includes(job.status)) {
                            btnHtml += `<button class="btn btn-sm btn-warning" onclick="event.stopPropagation(); pauseJob(${job.id})">停止</button>`;
                        } else {
                            btnHtml += `<button class="btn btn-sm btn-success" onclick="event.stopPropagation(); resumeJob(${job.id})">启动</button>`;
                            btnHtml += `<button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); editJob(${job.id})">修改</button>`;
                        }
                        btnHtml += `<button class="btn btn-sm btn-danger" onclick="event.stopPropagation(); deleteJob(${job.id})">删除</button>`;
                        btnHtml += '</div>';
                        actionTd.innerHTML = btnHtml;
                    }
                }
            });
        })
        .catch(err => console.error("Error updating jobs status:", err));
}

function pauseJob(jobId) {
    if (confirm(`确定要停止任务 #${jobId} 吗？`)) {
        fetch(`/api/jobs/${jobId}/pause`, { method: "POST" })
            .then(res => res.json())
            .then(() => updateJobsState())
            .catch(err => alert("停止任务失败: " + err));
    }
}

function resumeJob(jobId) {
    // 恢复/启动任务不需要额外确认
    fetch(`/api/jobs/${jobId}/resume`, { method: "POST" })
        .then(res => res.json())
        .then(() => {
            showToast(`任务 #${jobId} 已启动`, "success");
            updateJobsState();
        })
        .catch(err => alert("启动任务失败: " + err));
}

function deleteJob(jobId) {
    if (confirm(`确定要删除任务 #${jobId} 吗？`)) {
        fetch(`/api/jobs/${jobId}/delete`, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                showToast(data.message || "任务已成功删除", "success");
                const row = document.querySelector(`tr[data-job-id="${jobId}"]`) || document.getElementById(`job-tr-${jobId}`);
                if (row) {
                    row.remove();
                }
            })
            .catch(err => showToast("删除任务失败: " + err, "error"));
    }
}

function editJob(jobId) {
    fetch("/api/jobs")
        .then(res => res.json())
        .then(data => {
            const job = data.find(j => j.id === jobId);
            if (!job) {
                showToast("未找到该任务数据", "error");
                return;
            }
            
            document.getElementById("modal-job-id").innerText = jobId;
            document.getElementById("edit-job-id-input").value = jobId;
            
            const body = document.getElementById("modal-body-fields");
            body.innerHTML = "";
            
            let params = {};
            try {
                params = JSON.parse(job.params || "{}");
            } catch(e) {}
            
            if (job.kind === 'backtest') {
                const datasetStr = params.dataset_ids ? params.dataset_ids.join("\n") : "";
                body.innerHTML = `
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-dataset-ids" style="display:block; margin-bottom:6px; font-weight:500;">数据集 ID 列表 (每行输入一个)</label>
                        <textarea id="edit-dataset-ids" rows="5" class="form-control" style="width:100%; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-family:inherit; font-size:14px; box-sizing:border-box;">${datasetStr}</textarea>
                    </div>
                    <div class="form-group checkbox-group">
                        <label style="font-weight:500; display:block; margin-bottom:6px;">运行阶段：</label>
                        <div class="checkbox-options" style="display:flex; flex-direction:column; gap:10px;">
                            <label class="checkbox-label" style="display:flex; align-items:center; gap:8px; cursor:pointer;">
                                <input type="checkbox" id="edit-run-fo" ${params.run_fo !== false ? 'checked' : ''}>
                                <span>一阶 FO (算子因子化)</span>
                            </label>
                            <label class="checkbox-label" style="display:flex; align-items:center; gap:8px; cursor:pointer;">
                                <input type="checkbox" id="edit-run-so" ${params.run_so !== false ? 'checked' : ''}>
                                <span>二阶 SO (分组 neutralization 交叉)</span>
                            </label>
                            <label class="checkbox-label" style="display:flex; align-items:center; gap:8px; cursor:pointer;">
                                <input type="checkbox" id="edit-run-th" ${params.run_th !== false ? 'checked' : ''}>
                                <span>三阶 TH (交易控制过滤)</span>
                            </label>
                        </div>
                    </div>
                `;
            } else if (job.kind === 'catalog_refresh') {
                body.innerHTML = `
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-region" style="display:block; margin-bottom:6px; font-weight:500;">回测地区 (Region)</label>
                        <input type="text" id="edit-region" value="${params.region || 'USA'}" class="form-control" style="width:100%; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-size:14px; box-sizing:border-box;">
                    </div>
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-universe" style="display:block; margin-bottom:6px; font-weight:500;">股票池 (Universe)</label>
                        <input type="text" id="edit-universe" value="${params.universe || 'TOP3000'}" class="form-control" style="width:100%; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-size:14px; box-sizing:border-box;">
                    </div>
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-delay" style="display:block; margin-bottom:6px; font-weight:500;">延时 (Delay)</label>
                        <input type="number" id="edit-delay" value="${params.delay !== undefined ? params.delay : 1}" class="form-control" style="width:100%; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-size:14px; box-sizing:border-box;">
                    </div>
                `;
            } else if (job.kind === 'check_submission') {
                const manualStr = params.manual_ids ? params.manual_ids.join("\n") : "";
                body.innerHTML = `
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-manual-ids" style="display:block; margin-bottom:6px; font-weight:500;">待检查 Alpha ID 列表 (每行一个)</label>
                        <textarea id="edit-manual-ids" rows="5" class="form-control" style="width:100%; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-family:inherit; font-size:14px; box-sizing:border-box;">${manualStr}</textarea>
                    </div>
                `;
            } else {
                body.innerHTML = `
                    <div class="form-group" style="margin-bottom: 15px;">
                        <label for="edit-generic-json" style="display:block; margin-bottom:6px; font-weight:500;">任务参数 (JSON 格式)</label>
                        <textarea id="edit-generic-json" rows="8" class="form-control" style="width:100%; font-family:monospace; padding:10px; background:var(--bg-main); border:1px solid var(--border-color); color:var(--text-main); border-radius:6px; font-size:14px; box-sizing:border-box;">${JSON.stringify(params, null, 2)}</textarea>
                    </div>
                `;
            }
            
            document.getElementById("edit-job-modal").classList.add("active");
        })
        .catch(err => showToast("获取任务数据失败: " + err, "error"));
}

function closeEditModal() {
    document.getElementById("edit-job-modal").classList.remove("active");
}

function saveJobParams(event) {
    event.preventDefault();
    
    const jobId = document.getElementById("edit-job-id-input").value;
    
    // 二次确认机制
    const needConfirm = window.NEED_CONFIRM_ON_MODIFY === "1";
    if (needConfirm) {
        if (!confirm("确定要保存并修改该任务的参数配置吗？")) {
            return;
        }
    }
    
    let params = {};
    const datasetField = document.getElementById("edit-dataset-ids");
    const runFo = document.getElementById("edit-run-fo");
    const runSo = document.getElementById("edit-run-so");
    const runTh = document.getElementById("edit-run-th");
    
    const regionField = document.getElementById("edit-region");
    const universeField = document.getElementById("edit-universe");
    const delayField = document.getElementById("edit-delay");
    
    const manualField = document.getElementById("edit-manual-ids");
    const genericField = document.getElementById("edit-generic-json");
    
    if (datasetField) {
        params.dataset_ids = datasetField.value.split("\n").map(s => s.trim()).filter(s => s.length > 0);
        params.run_fo = runFo.checked;
        params.run_so = runSo.checked;
        params.run_th = runTh.checked;
    } else if (regionField) {
        params.region = regionField.value.trim();
        params.universe = universeField.value.trim();
        params.delay = parseInt(delayField.value) || 1;
    } else if (manualField) {
        params.manual_ids = manualField.value.split("\n").map(s => s.trim()).filter(s => s.length > 0);
    } else if (genericField) {
        try {
            params = JSON.parse(genericField.value);
        } catch(e) {
            showToast("无效的 JSON 格式，请检查", "error");
            return;
        }
    }
    
    const formData = new FormData();
    formData.append("params_json", JSON.stringify(params));
    
    fetch(`/api/jobs/${jobId}/modify`, {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        showToast(data.message || "任务参数修改成功", "success");
        closeEditModal();
        updateJobsState();
    })
    .catch(err => showToast("保存任务参数失败: " + err, "error"));
}

function refreshCatalog() {
    if (confirm("确定要刷新并同步重新生成本地数据目录缓存吗？这可能需要几分钟。")) {
        fetch("/api/jobs/catalog_refresh", { method: "POST" })
            .then(res => res.json())
            .then(data => {
                alert(`数据目录刷新任务已成功启动，任务 ID 为 #${data.job_id}。您可以到仪表盘查看进度。`);
                window.location.reload();
            })
            .catch(err => alert("启动更新任务失败: " + err));
    }
}

function importCredentials() {
    if (confirm("确定要读取本地 credentials.json 覆盖当前 WorldQuant 凭证配置吗？")) {
        fetch("/api/import_credentials", { method: "POST" })
            .then(res => res.json())
            .then(() => {
                alert("凭证导入成功！正在为您自动刷新页面。");
                window.location.reload();
            })
            .catch(err => alert("读取 credentials.json 失败，请检查文件是否存在: " + err));
    }
}

// ==========================================
// 详细日志实时滚动查看
// ==========================================

function viewJobDetails(jobId) {
    currentSelectedJobId = jobId;
    
    // 设置高亮行样式
    document.querySelectorAll(".job-row").forEach(r => r.classList.remove("active"));
    const activeRow = document.getElementById(`job-tr-${jobId}`);
    if (activeRow) activeRow.classList.add("active");
    
    // 显示面板并滚动展示
    const panel = document.getElementById("job-details-panel");
    panel.style.display = "block";
    const title = document.getElementById("details-job-title");
    if (title) {
        title.innerText = `任务详情 - Job #${jobId}`;
    }
    const selectedId = document.getElementById("selected-job-id-display");
    if (selectedId) {
        selectedId.innerText = jobId;
    }
    
    // 清理之前的定时器
    clearInterval(detailLogInterval);
    clearInterval(detailEventsInterval);
    
    // 立即更新并开启对应轮询
    updateJobLogs();
    updateJobEvents();
    detailLogInterval = setInterval(updateJobLogs, 2500); // 2.5 秒更新一次日志
    detailEventsInterval = setInterval(updateJobEvents, 5000); // 5 秒更新一次事件
    
    // 顺滑滚到详情面板
    panel.scrollIntoView({ behavior: 'smooth' });
}

function closeJobDetails() {
    document.getElementById("job-details-panel").style.display = "none";
    document.querySelectorAll(".job-row").forEach(r => r.classList.remove("active"));
    clearInterval(detailLogInterval);
    clearInterval(detailEventsInterval);
    currentSelectedJobId = null;
}

function switchDetailsTab(tab) {
    currentDetailsTab = tab;
    document.querySelectorAll(".details-body .tab-btn").forEach(b => b.classList.remove("active"));
    if (typeof event !== "undefined" && event.target) {
        event.target.classList.add("active");
    }
    const logTab = document.getElementById("tab-log");
    const eventsTab = document.getElementById("tab-events");
    const legacyLog = document.getElementById("job-log-content");
    const legacyEvents = document.getElementById("job-events-content");

    if (tab === 'log') {
        if (logTab && logTab.classList.contains("tab-content")) logTab.style.display = "block";
        if (eventsTab && eventsTab.classList.contains("tab-content")) eventsTab.style.display = "none";
        if (legacyLog) legacyLog.style.display = "block";
        if (legacyEvents) legacyEvents.style.display = "none";
    } else {
        if (logTab && logTab.classList.contains("tab-content")) logTab.style.display = "none";
        if (eventsTab && eventsTab.classList.contains("tab-content")) eventsTab.style.display = "block";
        if (legacyLog) legacyLog.style.display = "none";
        if (legacyEvents) legacyEvents.style.display = "block";
    }
}

function updateJobLogs() {
    if (!currentSelectedJobId) return;
    fetch(`/api/jobs/${currentSelectedJobId}/log_tail?max_lines=100`)
        .then(res => res.json())
        .then(data => {
            const viewer = document.getElementById("job-log-viewer") || document.getElementById("job-log-content");
            if (!viewer) return;
            viewer.innerText = data.lines.join("\n");
            
            // 是否开启自动滚动到底部
            const autoScroll = document.getElementById("auto-scroll-log");
            if (!autoScroll || autoScroll.checked) {
                viewer.scrollTop = viewer.scrollHeight;
            }
        })
        .catch(err => console.error("Error reading job log tail:", err));
}

function updateJobEvents() {
    if (!currentSelectedJobId) return;
    fetch(`/api/jobs/${currentSelectedJobId}/events`)
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById("job-events-list");
            const legacyContent = document.getElementById("job-events-content");
            if (!tbody && legacyContent) {
                if (data.length === 0) {
                    legacyContent.innerHTML = `<table class="table table-sm"><tbody><tr><td colspan="3" class="text-center text-muted">本任务当前没有后台事件记录</td></tr></tbody></table>`;
                    return;
                }
                const rowsHtml = data.map(e => {
                    let levelClass = 'secondary';
                    if (e.level === 'error') levelClass = 'danger';
                    if (e.level === 'warning') levelClass = 'warning';
                    if (e.level === 'info') levelClass = 'info';
                    return `
                        <tr>
                            <td class="text-xs text-muted">${escapeHtml(e.created_at || "")}</td>
                            <td><span class="badge ${levelClass}">${escapeHtml(e.level)}</span></td>
                            <td class="text-sm">${escapeHtml(e.message)}</td>
                        </tr>
                    `;
                }).join("");
                legacyContent.innerHTML = `
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead><tr><th>发生时间</th><th>等级</th><th>事件信息</th></tr></thead>
                            <tbody>${rowsHtml}</tbody>
                        </table>
                    </div>
                `;
                return;
            }
            if (data.length === 0) {
                tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">本任务目前没有记录任何后台事件</td></tr>`;
                return;
            }
            
            tbody.innerHTML = data.map(e => {
                const date = escapeHtml(e.created_at || "");
                let levelClass = 'secondary';
                if (e.level === 'error') levelClass = 'danger';
                if (e.level === 'warning') levelClass = 'warning';
                if (e.level === 'info') levelClass = 'info';
                
                return `
                    <tr>
                        <td class="text-xs text-muted">${date}</td>
                        <td><span class="badge ${levelClass}">${escapeHtml(e.level)}</span></td>
                        <td class="text-sm">${escapeHtml(e.message)}</td>
                    </tr>
                `;
            }).join("");
        })
        .catch(err => console.error("Error reading job events:", err));
}

// ==========================================
// 全局运行日志实时查看
// ==========================================

function startGuiLogTailing() {
    updateGuiLog();
    guiLogInterval = setInterval(updateGuiLog, 3000);
}

function updateGuiLog() {
    const viewer = document.getElementById("gui-log-viewer");
    if (!viewer) return;
    
    fetch("/api/gui_log_tail?max_lines=100")
        .then(res => res.json())
        .then(data => {
            viewer.innerText = data.lines.join("\n");
            if (document.getElementById("auto-scroll-gui-log").checked) {
                viewer.scrollTop = viewer.scrollHeight;
            }
        })
        .catch(err => console.error("Error updating GUI log tail:", err));
}

// ==========================================
// 浮动 Toast 提示组件
// ==========================================

function showToast(message, type = "success") {
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container";
        document.body.appendChild(container);
    }
    
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    
    const icon = type === "success" ? "fa-circle-check" : "fa-circle-xmark";
    toast.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // 触发回流动画
    toast.offsetHeight;
    
    toast.classList.add("show");
    
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => {
            toast.remove();
        }, 350);
    }, 4000);
}

// 绑定折叠卡片点击展开与隐藏的处理逻辑
document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", (e) => {
        const header = e.target.closest(".card-header.collapsible");
        if (header) {
            const card = header.closest(".card");
            if (card) {
                card.classList.toggle("collapsed");
            }
        }
    });

    // 恢复保存的滚动位置 (用于翻页和过滤不弹回顶部)
    const savedScrollPos = sessionStorage.getItem("scroll_pos_" + window.location.pathname);
    if (savedScrollPos !== null) {
        window.scrollTo(0, parseInt(savedScrollPos));
        // 延迟一小段时间再次确认（防止 DOM 异步渲染高度变化导致滚动失败）
        setTimeout(() => {
            window.scrollTo(0, parseInt(savedScrollPos));
            sessionStorage.removeItem("scroll_pos_" + window.location.pathname);
        }, 80);
    }
});

// 点击翻页、过滤或表单操作时记录当前滚动位置
document.addEventListener("click", (e) => {
    if (e.target.closest(".pagination") || 
        e.target.closest(".filter-bar") || 
        e.target.closest(".filter-group-buttons") || 
        e.target.closest(".filter-group-date-buttons") || 
        e.target.closest(".rename-inline-form")) {
        sessionStorage.setItem("scroll_pos_" + window.location.pathname, window.scrollY);
    }
});

// 下拉框选择过滤条件变更时记录滚动位置
document.addEventListener("change", (e) => {
    if (e.target.id === "level_filter_select") {
        sessionStorage.setItem("scroll_pos_" + window.location.pathname, window.scrollY);
    }
});

// 分页输入框回车提交时记录滚动位置
document.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && e.target.id === "jump-page-input") {
        sessionStorage.setItem("scroll_pos_" + window.location.pathname, window.scrollY);
    }
});
