
import sys
import os
import statistics

# Add the project root to the python path to import core logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs_optimizer.core import labs_cost, generate_random_sequence, solve_labs_random_restart

def run_experiment():
    print("========================================")
    print("   LABS Optimization Baseline Experiment")
    print("========================================")

    N = 30  # Sequence length as per requirements
    NUM_TRIALS = 20 # Number of trials for statistics
    RESTARTS_PER_TRIAL = 10 # Restarts for the optimizer per trial

    print(f"Configuration:")
    print(f"  Sequence Length (N): {N}")
    print(f"  Number of Trials: {NUM_TRIALS}")
    print(f"  Restarts in Optimizer: {RESTARTS_PER_TRIAL}")
    print("========================================\n")

    # --- Phase 1: Random Baseline ---
    print(f"Running {NUM_TRIALS} Random Baseline Trials...")
    random_costs = []
    for i in range(NUM_TRIALS):
        seq = generate_random_sequence(N)
        cost = labs_cost(seq)
        random_costs.append(cost)

    print(f"Random Baseline completed. Average Cost: {statistics.mean(random_costs):.2f}\n")

    # --- Phase 2: Optimizer Baseline ---
    print(f"Running {NUM_TRIALS} Optimizer Trials (Random-Restart Hill Climbing)...")
    optimized_costs = []
    
    for i in range(NUM_TRIALS):
        print(f"\n[Trial {i+1}/{NUM_TRIALS}]")
        # Using the existing optimizer function
        best_seq, best_cost = solve_labs_random_restart(N, num_restarts=RESTARTS_PER_TRIAL)
        optimized_costs.append(best_cost)
        print(f">> Trial {i+1} Final Result: {best_cost}")

    # --- Phase 3: Analysis & Reporting ---
    print("\n\n========================================")
    print("           EXPERIMENT RESULTS")
    print("========================================")

    print("\n--- Raw Data ---")
    print(f"Random Costs:    {random_costs}")
    print(f"Optimized Costs: {optimized_costs}")

    avg_rand = statistics.mean(random_costs)
    min_rand = min(random_costs)
    max_rand = max(random_costs)
    
    # Calculate median for robustness
    med_rand = statistics.median(random_costs)

    avg_opt = statistics.mean(optimized_costs)
    min_opt = min(optimized_costs)
    max_opt = max(optimized_costs)
    med_opt = statistics.median(optimized_costs)

    print("\n--- Summary Statistics ---")
    print(f"{'Metric':<15} | {'Random':<15} | {'Optimized':<15}")
    print("-" * 50)
    print(f"{'Average Cost':<15} | {avg_rand:<15.2f} | {avg_opt:<15.2f}")
    print(f"{'Median Cost':<15} | {med_rand:<15.2f} | {med_opt:<15.2f}")
    print(f"{'Best (Min)':<15} | {min_rand:<15} | {min_opt:<15}")
    print(f"{'Worst (Max)':<15} | {max_rand:<15} | {max_opt:<15}")
    
    diff = avg_rand - avg_opt
    pct_imp = (diff / avg_rand) * 100 if avg_rand > 0 else 0
    
    print("-" * 50)
    print(f"Improvement: {diff:.2f} points ({pct_imp:.1f}%)")
    
    # Simple Text Visualization
    print("\n--- Cost Comparison (Ascending Sort) ---")
    sorted_rand = sorted(random_costs)
    sorted_opt = sorted(optimized_costs)
    
    for i in range(NUM_TRIALS):
        r_val = sorted_rand[i]
        o_val = sorted_opt[i]
        print(f"Rank {i+1:2}: Random {r_val:4}  vs  Optimized {o_val:4}")

    print("\n--- Cost Histogram (Text-Based) ---")
    def print_hist(label, data, char='*'):
        print(f"\n{label}:")
        if not data: return
        min_v, max_v = min(data), max(data)
        # Create bins
        bins = 10
        width = (max_v - min_v) / bins if max_v > min_v else 1
        
        hist = [0] * (bins + 1)
        for v in data:
            idx = int((v - min_v) / width)
            idx = min(idx, bins)
            hist[idx] += 1
            
        for i in range(bins + 1):
            range_start = min_v + i * width
            range_end = min_v + (i + 1) * width
            if i == bins:
                print(f"[{range_start:6.1f}+       ] | {''.join([char]*hist[i])} ({hist[i]})")
            else:
                print(f"[{range_start:6.1f}-{range_end:6.1f}] | {''.join([char]*hist[i])} ({hist[i]})")

    print_hist("Random Costs", random_costs, char='#')
    print_hist("Optimized Costs", optimized_costs, char='@')

if __name__ == "__main__":
    run_experiment()
