# TTR Prompting (Think Then Respond)

A simple yet effective prompting strategy for improved LLM reasoning.

## Overview

**TTR (Think Then Respond)** is a two-stage prompting approach that guides language models to:
1. Think through their reasoning step by step
2. Provide a final response based on that reasoning

## Results on MMLU

| Model | Score |
|-------|--------|
| GPT-4 | 92.3% |
| **Llama 3.1 405B (TTR)** | **91.7%** |
| DeepSeek R1 (64 attempts) | 90.8% |
| DeepSeek V3 | 88.5% |
| Claude 3.5 Sonnet | 88.3% |
| GPT-4 0513 | 87.2% |

Notable that TTR achieves 91.7% with a single pass, compared to DeepSeek R1's 90.8% which requires 64 attempts per question.

## Implementation

The approach uses two prompts:
```python
thought_prompt = "How should you best think about this? Explain your thought process step by step."

output_format = "Output only a single digit representing your choice (with no additional commentary)"
```

## Example Outputs

### Mathematical Reasoning
```
Q: How long does it take scientists at the Centre to make sure a cocoa plant is safe to grow?

[Options]
0. 6 months
1. 12 months
2. 24 months
3. 30 months

Thinking process:
1. The text states that each new plant is stored at the Control Centre for six months
2. After the initial six months, the plant is then planted in the Centre's fields, studied, and tested for another two years
3. Calculate total time:
   - Initial storage: 6 months
   - Testing in fields: 2 years = 24 months
   - Total: 6 + 24 = 30 months

Answer: 3
```

### Logical Deduction
```
Q: Where did the salt for the hotel come from?

[Options]
0. A cave
1. The lake
2. The salt desert
3. A salt field

Thinking process:
1. The hotel is located in Bolivia, in an area that was once a large lake but now has two small lakes and two salt deserts
2. The text states that Juan Quesada "cut big blocks of salt from the desert" to build the hotel
3. This directly indicates the source of the salt

Answer: 2
```

## Hardware Used
Testing performed on Lambda Labs cloud instance:
- 8x A100 (80 GB SXM4)
- 240 CPU cores
- 1.9 TB RAM
- 22 TB SSD
- Cost: $14.32/hr ($1.79/GPU/hr)

## Model Details
- Model: Meta-Llama-3.1-405B-Instruct
- Quantization: AWQ-INT4

## Usage

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python src/main.py <num_threads>`

## License

MIT License
