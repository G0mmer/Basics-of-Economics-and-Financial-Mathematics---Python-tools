import matplotlib.pyplot as plt
import numpy as np

def plot_annuity_valuation(n, P, i, m_defer=0, m_post=0, eval_point=0, annuity_type='immediate', plot_type='pv'):
    """
    Plots a single annuity valuation graph based on the plot_type: 'pv', 'fv', or 'current'.
    Also prints the calculated variables to the console.
    """
    # Core Calculations
    v = 1 / (1 + i)
    d = i / (1 + i)
    pv_factor = (1 - v**n) / i if annuity_type == 'immediate' else (1 - v**n) / d
    
    # Determine timelines based on annuity type
    if annuity_type == 'immediate':
        pay_times = np.arange(1, n + 1)
        last_pay_t = m_defer + n
    else:
        pay_times = np.arange(0, n)
        last_pay_t = m_defer + n - 1
        
    pay_times_deferred = pay_times + m_defer
    total_max_time = last_pay_t + m_post
    
    # Values
    pv_m = P * pv_factor
    pv_0 = pv_m * (v**m_defer)
    
    t_discrete = np.arange(0, total_max_time + 1)
    value_curve = pv_0 * (1 + i)**t_discrete 
    
    fv_total = value_curve[-1]
    
    print("-" * 50)
    print(f"---Calculations Summary: {plot_type.upper()} ({annuity_type.upper()}) ---")
    print(f"Initial parameters: P={P}, n={n}, m_defer={m_defer}, m_post={m_post}")
    print(f"Interest rate. (i) = {i:.6f} ({i*100}%)")
    print(f"Discount factor. (v) = {v:.6f}")
    print(f"Discount rate. (d) = {d:.6f}")
    print("- - -")
    print(f"PV at t=0: ${pv_0:.2f}")
    print(f"FV at t={total_max_time}: ${fv_total:.2f}")
    
    if plot_type == 'pv':
        print(f"PV before the annuity (t={m_defer}): ${pv_m:.2f}")
        print(f"PV today (t=0): ${pv_0:.2f}")
    elif plot_type == 'fv':
        fv_n = value_curve[last_pay_t]
        print(f"FV after the last payment (t={last_pay_t}): ${fv_n:.2f}")
        if m_post > 0:
            print(f"FV postopned at (t={total_max_time}): ${fv_total:.2f}")
    elif plot_type == 'current':
        current_val = value_curve[eval_point]
        print(f"Current value at (t={eval_point}): ${current_val:.2f}")
    print("-" * 50)
    

    # Setup Figure
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hlines(0, 0, total_max_time + 0.5, color='black', linewidth=1.5)
    ax.plot(t_discrete, value_curve, 'o--', color='orange', alpha=0.6, label='Equivalent Value Trend $(1+i)^t$')
    
    # Annotate global PV and FV on the curve
    ax.annotate(f'PV (Start)\n${pv_0:.2f}', (0, pv_0), textcoords="offset points", xytext=(-10, 15), 
                ha='right', va='bottom', color='darkorange', fontweight='bold')
    ax.annotate(f'FV (End)\n${fv_total:.2f}', (total_max_time, fv_total), textcoords="offset points", xytext=(10, 15), 
                ha='left', va='bottom', color='darkorange', fontweight='bold')

    # Plot Payments
    # Separate past vs future payments if it's a current value plot
    if plot_type == 'current':
        past_pays = [t for t in pay_times_deferred if t <= eval_point]
        future_pays = [t for t in pay_times_deferred if t > eval_point]
        if past_pays:
            markerline, stemlines, baseline = ax.stem(past_pays, np.full(len(past_pays), P), linefmt='gray', markerfmt='o')
            plt.setp(baseline, visible=False)
        if future_pays:
            markerline, stemlines, baseline = ax.stem(future_pays, np.full(len(future_pays), P), linefmt='b-', markerfmt='bo')
            plt.setp(baseline, visible=False)
    else:
        markerline, stemlines, baseline = ax.stem(pay_times_deferred, np.full(n, P), linefmt='b-', markerfmt='bo')
        plt.setp(baseline, visible=False)

    # Add payment amounts explicitly above the dots
    for t in pay_times_deferred:
        color = 'gray' if (plot_type == 'current' and t <= eval_point) else 'blue'
        ax.annotate(f'+${P}', (t, P), textcoords="offset points", xytext=(0, 10), 
                    ha='center', va='bottom', color=color, fontweight='bold', fontsize=8)

    # Type-Specific Annotations
    arrow_y = value_curve[-1] * 1.15
    
    if plot_type == 'pv':
        ax.set_title(f'Present Value (Deferred for m={m_defer} periods)', fontweight='bold', pad=15)
        ax.plot(m_defer, pv_m, 'go', markersize=9)
        ax.plot(0, pv_0, 'ro', markersize=9)
        
        ax.annotate(f'Value at t={m_defer}\n${pv_m:.2f}', (m_defer, pv_m), textcoords="offset points", 
                     xytext=(0, -35), ha='center', va='top', color='green', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green"))
        ax.annotate(f'Discounted PV\n${pv_0:.2f}', (0, pv_0), textcoords="offset points", 
                     xytext=(0, -35), ha='center', va='top', color='red', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=2))
                     
        if m_defer > 0:
            ax.annotate('', xy=(0, arrow_y), xytext=(m_defer, arrow_y), arrowprops=dict(facecolor='red', shrink=0, width=2, headwidth=8))
            ax.text(m_defer/2, arrow_y + P*0.05, 'Discount backward (v)', ha='center', va='bottom', color='red', fontweight='bold')

    elif plot_type == 'fv':
        fv_n = value_curve[last_pay_t]
        
        ax.set_title(f'Accumulated Value (m={m_post} periods post-annuity)', fontweight='bold', pad=15)
        ax.plot(last_pay_t, fv_n, 'o', color='darkorange', markersize=9)
        ax.plot(total_max_time, fv_total, 'ro', markersize=9)
        
        ax.annotate(f'Accumulated at t={last_pay_t}\n${fv_n:.2f}', (last_pay_t, fv_n), textcoords="offset points", 
                     xytext=(0, -35), ha='center', va='top', color='darkorange', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="orange"))
        ax.annotate(f'Final FV\n${fv_total:.2f}', (total_max_time, fv_total), textcoords="offset points", 
                     xytext=(0, -35), ha='center', va='top', color='red', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=2))
                     
        if m_post > 0:
            ax.annotate('', xy=(total_max_time, arrow_y), xytext=(last_pay_t, arrow_y), arrowprops=dict(facecolor='red', shrink=0, width=2, headwidth=8))
            ax.text((last_pay_t + total_max_time)/2, arrow_y + P*0.05, 'Accumulate forward (1+i)', ha='center', va='bottom', color='red', fontweight='bold')

    elif plot_type == 'current':
        current_val = value_curve[eval_point]
        ax.set_title(f'Current Value (Evaluated at midway t={eval_point})', fontweight='bold', pad=15)
        
        ax.plot(eval_point, current_val, 'mo', markersize=10)
        ax.axvline(x=eval_point, color='purple', linestyle='--', alpha=0.4)
        
        ax.annotate(f'Equation of Value at t={eval_point}\n${current_val:.2f}', (eval_point, current_val), 
                     textcoords="offset points", xytext=(0, -45), ha='center', va='top', color='purple', 
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="purple", lw=2))

    # Formatting
    ax.set_xlabel('Time (Periods)', fontweight='bold')
    ax.set_xlim(-1, total_max_time + 1)
    ax.set_ylim(-P*0.3, value_curve[-1] * 1.5) 
    
    # Adjust x-ticks if there are too many (e.g. >15)
    if len(t_discrete) > 15:
        ax.set_xticks(t_discrete[::2])
    else:
        ax.set_xticks(t_discrete)
        
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    plt.show()