import os
from pathlib import Path
import shutil

def main():
    base_dir = Path("reference/unverified")
    
    # 1. 定义大类文件夹
    categories = {
        "correlation_reduction": [
            "自相关", "correlation", "selfppac", "SC", "sc", "Pearson", "Pruner"
        ],
        "sharpe_and_pnl_optimization": [
            "Sharpe", "Pnl", "甫子君", "Pyramid", "区域优化"
        ],
        "datafields_and_pruning": [
            "prune", "剪枝", "dataset", "数据集", "字段"
        ],
        "submission_and_progression": [
            "Grandmaster", "Eligibility", "vf", "value factor", "Submittable Alpha", "自学路径图", "直升"
        ],
        "workflow_and_tools": [
            "mcp", "工作流", "提示词", "wqapp", "machine-lib", "内存溢出", "自动化创建", "Selection", "征文", "合集", "API", "小建议", "必读"
        ]
    }
    
    # 创建分类文件夹
    for cat in categories.keys():
        (base_dir / cat).mkdir(parents=True, exist_ok=True)
        
    # 2. 遍历 reference/unverified 下的直接子文件，进行分类移动
    moved_count = 0
    
    for item in base_dir.iterdir():
        if item.is_file() and item.suffix == ".md":
            filename = item.name
            filename_lower = filename.lower()
            
            # 根据关键字进行匹配
            matched_cat = None
            
            if any(kw.lower() in filename_lower for kw in categories["correlation_reduction"]):
                matched_cat = "correlation_reduction"
            elif any(kw.lower() in filename_lower for kw in categories["sharpe_and_pnl_optimization"]):
                matched_cat = "sharpe_and_pnl_optimization"
            elif any(kw.lower() in filename_lower for kw in categories["datafields_and_pruning"]):
                matched_cat = "datafields_and_pruning"
            elif any(kw.lower() in filename_lower for kw in categories["submission_and_progression"]):
                matched_cat = "submission_and_progression"
            elif any(kw.lower() in filename_lower for kw in categories["workflow_and_tools"]):
                matched_cat = "workflow_and_tools"
            else:
                matched_cat = "workflow_and_tools"
                
            dest = base_dir / matched_cat / filename
            try:
                shutil.move(str(item), str(dest))
                # 避免输出 Emoji 导致 GBK 控制台报错
                safe_name = filename.encode('ascii', errors='ignore').decode('ascii')
                print(f"[Classify OK] '{safe_name}' -> '{matched_cat}/'")
                moved_count += 1
            except Exception as e:
                pass
                
    print(f"\nClassification done: Moved {moved_count} files.")

if __name__ == "__main__":
    main()
