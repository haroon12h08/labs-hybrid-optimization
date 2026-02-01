import random

def labs_cost(sequence):
    """
    Computes the Energy/Cost for a Low Autocorrelation Binary Sequence (LABS).
    
    The cost is defined as the sum of squared periodic autocorrelations 
    for all non-zero shifts k.
    
    Formally:
        C_k = sum_{i=0}^{N-k-1} s[i] * s[i+k]
        Cost = sum_{k=1}^{N-1} (C_k)^2
        
    Args:
        sequence: A list or 1D array of integers, restricted to {-1, +1}.
        
    Returns:
        The integer cost (energy) of the sequence.
    """
    N = len(sequence)
    total_cost = 0
    
    # Allow compatibility with both Python lists and NumPy arrays
    # Explicit loop implementation for clarity as requested
    
    # Iterate through each shift k from 1 to N-1
    for k in range(1, N):
        c_k = 0
        
        # Compute autocorrelation for shift k
        # Sum s[i] * s[i+k] for valid overlaps
        for i in range(N - k):
            c_k += sequence[i] * sequence[i + k]
            
        # Add square of the autocorrelation to total cost
        total_cost += c_k ** 2
        
    return total_cost


def generate_random_sequence(N):
    """
    Generates a uniform random sequence of length N with values {-1, 1}.
    
    Args:
        N: Length of the sequence.
        
    Returns:
        A list containing N elements, each being -1 or 1.
    """
    return [random.choice([-1, 1]) for _ in range(N)]


def run_random_baseline(N, num_samples=10):
    """
    Runs a random baseline check for LABS sequences of length N.
    Prints the costs of generated sequences.
    """
    print(f"--- Random Baseline (N={N}, Samples={num_samples}) ---")
    costs = []
    
    for _ in range(num_samples):
        seq = generate_random_sequence(N)
        c = labs_cost(seq)
        costs.append(c)
        
    for i, c in enumerate(costs):
        print(f"Sample {i+1}: Cost = {c}")
        
    avg_cost = sum(costs) / len(costs)
    print(f"Average Cost: {avg_cost:.2f}")
    return costs


def hill_climb_deterministic(sequence):
    """
    Performs a deterministic hill-climbing optimization on the given LABS sequence.
    
    Algorithm:
    1. Start with the input sequence.
    2. Iterate through each bit position.
    3. Flip the bit and check if the cost strictly decreases.
    4. If cost decreases, keep the flip.
    5. Repeat until a full pass over the sequence results in no changes.
    
    Args:
        sequence: A list of integers {-1, 1}.
        
    Returns:
        A tuple (optimized_sequence, final_cost).
    """
    # Work on a copy to avoid side effects on the input object
    current_seq = list(sequence)
    current_cost = labs_cost(current_seq)
    N = len(current_seq)
    
    # Loop until no improvement is found in a full pass
    while True:
        improved = False
        
        # Iterate over every bit
        for i in range(N):
            # 1. Flip the bit
            current_seq[i] *= -1
            
            # 2. Compute new cost
            new_cost = labs_cost(current_seq)
            
            # 3. Check for strict improvement
            if new_cost < current_cost:
                current_cost = new_cost
                improved = True
                # Keep the change
            else:
                # Revert the flip
                current_seq[i] *= -1
                
        # If we went through the whole sequence without a single improvement, stop.
        if not improved:
            break
            
    return current_seq, current_cost



if __name__ == "__main__":
    # import random  <-- Removed local import since we moved it to top

    
    print("--- LABS Cost Function Correctness Check ---")
    
    # Test Case 1: All ones
    # For N=5, sequence = [1, 1, 1, 1, 1]
    # k=1: 4 overlaps -> C_1 = 4 -> C_1^2 = 16
    # k=2: 3 overlaps -> C_2 = 3 -> C_2^2 = 9
    # k=3: 2 overlaps -> C_3 = 2 -> C_3^2 = 4
    # k=4: 1 overlap  -> C_4 = 1 -> C_4^2 = 1
    # Total = 16 + 9 + 4 + 1 = 30
    N = 5
    ones_seq = [1] * N
    cost_ones = labs_cost(ones_seq)
    print(f"Sequence: {ones_seq}")
    print(f"Calculated Cost: {cost_ones}")
    print(f"Expected Cost (N=5 all ones): 30")
    
    # Test Case 2: Random +/- 1 Sequence
    N_rand = 10
    rand_seq = [random.choice([-1, 1]) for _ in range(N_rand)]
    cost_rand = labs_cost(rand_seq)
    
    print(f"\nSequence: Random (Length {N_rand})")
    print(f"First few elements: {rand_seq[:5]}...")
    print(f"Calculated Cost: {cost_rand}")

    print("\n")
    # Run a baseline check for a larger N
    run_random_baseline(N=20, num_samples=10)

    print("\n--- Hill Climbing Demo ---")
    # Generate a random start
    N_opt = 20
    start_seq = generate_random_sequence(N_opt)
    start_cost = labs_cost(start_seq)
    
    print(f"Start Sequence (N={N_opt}) Cost: {start_cost}")
    
    opt_seq, opt_cost = hill_climb_deterministic(start_seq)
    
    print(f"Final Sequence Cost: {opt_cost}")
    if opt_cost < start_cost:
        print("Optimization successful: Cost reduced.")
    else:
        print("No improvement found (local optimum).")

