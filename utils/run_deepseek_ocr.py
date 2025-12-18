"""
Q6 AI 입국 심사관 - DeepSeek-OCR을 사용하여 PDF에서 텍스트 추출
30명 신청자의 7종 서류(여권, 비자, 입국신고서, 항공권, 건강증명서, 재정증명서, 세관신고서) 처리
"""
import os
import sys
import io
import glob
import warnings
warnings.filterwarnings('ignore')

# Step 1: PDF를 이미지로 변환
def convert_pdfs_to_images():
    """모든 신청자의 PDF를 이미지로 변환"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF not installed. Run: pip install pymupdf")
        return False

    base_path = "applicants"
    applicants = sorted([d for d in os.listdir(base_path) if d.startswith('applicant_')])

    total_converted = 0
    for app_id in applicants:
        app_path = os.path.join(base_path, app_id)
        images_dir = os.path.join(app_path, "images")
        os.makedirs(images_dir, exist_ok=True)

        pdf_files = glob.glob(os.path.join(app_path, "*.pdf"))

        for pdf_path in pdf_files:
            pdf_name = os.path.basename(pdf_path).replace('.pdf', '')

            try:
                doc = fitz.open(pdf_path)
                for page_num, page in enumerate(doc):
                    # 고해상도 이미지로 변환 (300 DPI)
                    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                    pix = page.get_pixmap(matrix=mat)

                    output_path = os.path.join(images_dir, f"{pdf_name}_page{page_num+1}.png")
                    pix.save(output_path)
                    total_converted += 1
                doc.close()
            except Exception as e:
                print(f"Error converting {pdf_path}: {e}")

    print(f"Converted {total_converted} PDF pages to images")
    return True


# Step 2: DeepSeek-OCR로 텍스트 추출
def load_model():
    """DeepSeek-OCR 모델 로드"""
    import torch
    from transformers import AutoModel, AutoTokenizer

    os.environ["CUDA_VISIBLE_DEVICES"] = '0'

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
    lines = output_str.split('\n')
    text_lines = []
    for line in lines:
        line = line.strip()
        if '<|ref|>' in line or '<|det|>' in line:
            continue
        if line.startswith('BASE:') or line.startswith('PATCHES:') or line.startswith('==='):
            continue
        if line:
            text_lines.append(line)
    return '\n'.join(text_lines)


def capture_infer_output(model, tokenizer, prompt, image_file, output_path):
    """infer 호출 시 stdout을 캡처하여 텍스트 추출"""
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

    sys.stdout = old_stdout
    output = captured_output.getvalue()
    return extract_text_from_output(output)


def run_ocr():
    """모든 신청자 이미지에 OCR 수행"""
    base_path = "applicants"
    applicants = sorted([d for d in os.listdir(base_path) if d.startswith('applicant_')])

    # 모델 로드
    model, tokenizer = load_model()
    prompt = "<image>\n<|grounding|>Convert the document to markdown."

    for app_id in applicants:
        app_path = os.path.join(base_path, app_id)
        images_dir = os.path.join(app_path, "images")
        ocr_output_dir = os.path.join(app_path, "ocr_output")
        os.makedirs(ocr_output_dir, exist_ok=True)

        if not os.path.exists(images_dir):
            print(f"No images directory for {app_id}, skipping...")
            continue

        image_files = glob.glob(os.path.join(images_dir, "*.png"))

        print(f"\n=== Processing {app_id} ({len(image_files)} images) ===")

        all_results = []
        for img_path in sorted(image_files):
            img_name = os.path.basename(img_path)
            print(f"  OCR: {img_name}", end=" ", flush=True)

            try:
                text = capture_infer_output(model, tokenizer, prompt, img_path, ocr_output_dir)

                if text:
                    all_results.append(f"=== {img_name} ===\n{text}\n")
                    print(f"-> {len(text)} chars")
                else:
                    all_results.append(f"=== {img_name} ===\n[No text extracted]\n")
                    print("-> No text")
            except Exception as e:
                print(f"-> Error: {e}")
                all_results.append(f"=== {img_name} ===\n[Error: {e}]\n")

        # 결과 저장
        output_file = os.path.join(app_path, "ocr_content.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_results))

        print(f"  Saved: {output_file}")

    print("\n=== OCR completed for all applicants! ===")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Q6 AI Immigration - PDF OCR')
    parser.add_argument('--step', type=int, default=0,
                       help='1=Convert PDF to images, 2=Run OCR, 0=Both')
    args = parser.parse_args()

    if args.step == 0 or args.step == 1:
        print("=== Step 1: Converting PDFs to images ===")
        if not convert_pdfs_to_images():
            print("PDF conversion failed!")
            return

    if args.step == 0 or args.step == 2:
        print("\n=== Step 2: Running DeepSeek-OCR ===")
        run_ocr()


if __name__ == "__main__":
    main()
