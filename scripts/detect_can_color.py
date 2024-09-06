from PIL import Image
import pandas as pd
from transformers import AutoProcessor, LlavaForConditionalGeneration

pkl_path = '/coc/flash8/wshin49/droid/can_demos_with_colors.pkl'
df = pd.read_pickle(pkl_path)

model_name = "llava-hf/llava-1.5-7b-hf"
model = LlavaForConditionalGeneration.from_pretrained(f"{model_name}")
processor = AutoProcessor.from_pretrained(f"{model_name}")
# text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
prompt = "USER: <image>\nWhat's the color of the can in the image? Answer in just one adjective word. ASSISTANT:"

for index, row in df.iterrows():
    demo_id = row['Demo']
    print(f'demo_id: {demo_id}')
    try:
        image_path = f"/coc/flash8/wshin49/droid/images/can/{demo_id}.png"
        image = Image.open(image_path)

        inputs = processor(text=prompt, images=image, return_tensors="pt")
        generate_ids = model.generate(**inputs, max_new_tokens=15)
        ans = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        color = ans[0].split(" ")[-1]
    except:
        print(f"Error processing {demo_id}: {e}")
        color = None

    df.loc[index, 'Color'] = color

df.to_pickle(pkl_path)

