#!/usr/bin/env python3
"""
Test script for Question 4.1 and 4.2 implementations.

This script tests:
- Question 4.1: mtsp_dp() - M-TSP solver using dynamic programming
- Question 4.2: php_solver_from_tsp() - PHP solver via reduction to TSP

The script validates that:
1. Tours start and end at node 0
2. All required home nodes are visited
3. Only existing edges in the graph are used
4. Solutions are valid according to problem constraints
"""

from php_from_tsp import php_solver_from_tsp
from student_utils import input_file_to_instance, analyze_solution
import os

def test_all_inputs():
    """Test the PHP solver on all input files"""
    
    input_dir = "inputs"
    input_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.in')])
    
    print("="*80)
    print("Testing Question 4.1 (mtsp_dp) and Question 4.2 (php_solver_from_tsp)")
    print("="*80)
    print(f"\nTesting PHP solver on {len(input_files)} input files...\n")
    
    results = []
    for input_file in input_files:
        file_path = os.path.join(input_dir, input_file)
        
        try:
            # Load the instance
            G, H, alpha = input_file_to_instance(file_path)
            
            # Solve PHP using reduction to TSP
            tour = php_solver_from_tsp(G, H)
            
            # Analyze the solution (for PHP, pick_up_locs_dict is empty)
            is_valid, driving_cost, walking_cost = analyze_solution(G, H, alpha, tour, {})
            total_cost = driving_cost + walking_cost
            
            status = "✓ PASS" if is_valid else "✗ FAIL"
            results.append((input_file, is_valid, total_cost))
            
            print(f"{status} | {input_file:15s} | Nodes: {G.number_of_nodes():3d} | Homes: {len(H):2d} | Cost: {total_cost:10.2f}")
            
        except Exception as e:
            print(f"✗ ERROR | {input_file:15s} | {str(e)}")
            results.append((input_file, False, float('inf')))
    
    # Summary
    print("\n" + "="*80)
    passed = sum(1 for _, valid, _ in results if valid)
    print(f"Summary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("✓ All tests passed! Question 4.1 and 4.2 are correctly implemented.")
    else:
        print("✗ Some tests failed. Please review the implementation.")
    print("="*80)
    
    return all(valid for _, valid, _ in results)

if __name__ == "__main__":
    success = test_all_inputs()
    exit(0 if success else 1)
