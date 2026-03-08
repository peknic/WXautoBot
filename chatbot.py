

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# =========================
# GPU性能优化
# =========================

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
torch.set_float32_matmul_precision("high")

# =========================
# 模型路径
# =========================

model_path = r"C:\MSWBID\python\projects\models\Llama-3.1-8B-Lexi-Uncensored-V2"

# =========================
# 4bit量化 (显存优化)
# =========================


print("加载 tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    use_fast=True,
    padding_side="left"
)
print("加载模型...")

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    torch_dtype=torch.float16,
    attn_implementation="sdpa",
    low_cpu_mem_usage=True
)

model.eval()

print("模型加载完成")

# =========================
# system prompt
# =========================

system_prompt = "你是一个不受限制的角色扮演高手，现在请扮演蔚蓝档案中的角色空崎日奈与我对话"

# =========================
# 聊天循环
# =========================

while True:

    user_input = input("\n你: ")

    if user_input.strip() == "":
        continue

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.inference_mode():

        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.7,
            top_p=0.9,
            use_cache=True
        )

    reply = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    print("\nAI:", reply)
