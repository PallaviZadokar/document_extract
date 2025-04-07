from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Load model & processor
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

def extract_using_donut(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    task_prompt = "<s_docvqa><s_question>Extract all key-value fields from this document</s_question><s_answer>"
    
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    outputs = model.generate(pixel_values, decoder_input_ids=decoder_input_ids, max_length=512)

    result = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return result






