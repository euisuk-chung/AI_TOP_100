"""
DeepSeek-OCR을 사용하여 PDF 이미지에서 텍스트 추출
"""
import os
import sys
import io
import torch
from transformers import AutoModel, AutoTokenizer
import glob
import re
import warnings
warnings.filterwarnings('ignore')

# GPU 설정
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

def load_model():
    """DeepSeek-OCR 모델 로드"""
    model_name = 'deepseek-ai/DeepSeek-OCR'
    print(f"Loading model: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True,
        use_safetensors=True,
        torch_dtype=torch.bfloat16,
        device_map='auto'
    )
    model = model.eval()
    print("Model loaded successfully!")
    print(f"GPU memory used: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
    return model, tokenizer

def extract_text_from_output(output_str):
    """OCR 출력에서 텍스트만 추출"""
    # <|ref|>...<|/ref|><|det|>...<|/det|> 패턴 제거하고 텍스트만 추출
    # 줄바꿈으로 분리하고 # 또는 텍스트로 시작하는 줄만 추출
    lines = output_str.split('\n')
    text_lines = []
    for line in lines:
        line = line.strip()
        # ref/det 태그가 있는 줄은 건너뜀
        if '<|ref|>' in line or '<|det|>' in line:
            continue
        # BASE, PATCHES 같은 디버그 출력 건너뜀
        if line.startswith('BASE:') or line.startswith('PATCHES:') or line.startswith('==='):
            continue
        if line:
            text_lines.append(line)
    return '\n'.join(text_lines)

def capture_infer_output(model, tokenizer, prompt, image_file, output_path):
    """infer 호출 시 stdout을 캡처하여 텍스트 추출"""
    # stdout 캡처
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()

    try:
        model.infer(
            tokenizer,
            prompt=prompt,
            image_file=image_file,
            output_path=output_path,
            base_size=1024,
            image_size=640,
            crop_mode=True,
            save_results=False,
            test_compress=False
        )
    except Exception as e:
        pass

    # stdout 복원
    sys.stdout = old_stdout
    output = captured_output.getvalue()

    # 텍스트 추출
    return extract_text_from_output(output)

def main():
    # PDF 1 이미지 폴더
    images_dir = "pdf_1/images"
    output_dir = "pdf_1/ocr_output"
    os.makedirs(output_dir, exist_ok=True)

    # 이미지 파일 목록 (페이지 순서로 정렬)
    image_files = glob.glob(os.path.join(images_dir, "*"))

    # 페이지 번호로 정렬
    def get_page_num(path):
        name = os.path.basename(path)
        try:
            return int(name.split('_')[0].replace('page', ''))
        except:
            return 0
    image_files = sorted(image_files, key=get_page_num)

    print(f"Found {len(image_files)} images")
    if not image_files:
        print("No images found!")
        return

    # 모델 로드
    model, tokenizer = load_model()

    # 프롬프트
    prompt = "<image>\n<|grounding|>Convert the document to markdown."

    # 각 이미지에서 텍스트 추출
    all_results = []
    for i, img_path in enumerate(image_files):
        page_name = os.path.basename(img_path)
        print(f"Processing {i+1}/{len(image_files)}: {page_name}", end=" ", flush=True)

        try:
            text = capture_infer_output(model, tokenizer, prompt, img_path, output_dir)

            if text:
                all_results.append(f"=== Page: {page_name} ===\n{text}\n")
                print(f"-> {len(text)} chars")
            else:
                all_results.append(f"=== Page: {page_name} ===\n[No text extracted]\n")
                print("-> No text")

        except Exception as e:
            print(f"-> Error: {e}")
            all_results.append(f"=== Page: {page_name} ===\n[Error: {e}]\n")

    # 전체 결과 저장
    output_file = "pdf_1/ocr_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_results))

    print(f"\nOCR completed! Output saved to: {output_file}")

if __name__ == "__main__":
    main()
