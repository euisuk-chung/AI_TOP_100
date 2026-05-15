"""
Q5 PDF 속 텍스트 추적 - PDF 분석 도구
숨겨진 텍스트, 이미지 오버랩, 비정상 폰트/색상 탐지
"""
import fitz  # PyMuPDF
from pathlib import Path


def analyze_pdf(pdf_path, verbose=True):
    """
    PDF 분석: 숨겨진 텍스트, 이미지 오버랩, 비정상 요소 탐지

    Args:
        pdf_path: PDF 파일 경로
        verbose: 상세 출력 여부

    Returns:
        dict: 분석 결과
    """
    doc = fitz.open(pdf_path)
    results = {
        "total_pages": len(doc),
        "suspicious_texts": [],
        "image_overlaps": [],
        "hidden_texts": [],
        "metadata": doc.metadata
    }

    for page_num, page in enumerate(doc):
        if verbose:
            print(f"\n=== Page {page_num + 1} ===")

        # 텍스트 블록 분석
        page_dict = page.get_text("dict")
        blocks = page_dict.get("blocks", [])

        # 이미지 영역 추출
        image_bboxes = [b["bbox"] for b in blocks if b["type"] == 1]

        for b in blocks:
            if b["type"] != 0:  # 텍스트 블록만
                continue

            for line in b["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    color = span["color"]
                    size = span["size"]
                    font = span["font"]
                    bbox = span["bbox"]

                    # 비정상 텍스트 탐지
                    is_suspicious = False
                    reasons = []

                    # 1. 흰색 텍스트 (숨김 의심)
                    if color == 16777215:  # 0xFFFFFF
                        is_suspicious = True
                        reasons.append("white_text")

                    # 2. 매우 작은 폰트
                    if size < 5:
                        is_suspicious = True
                        reasons.append("tiny_font")

                    # 3. 이미지와 오버랩
                    for img_bbox in image_bboxes:
                        if (bbox[0] < img_bbox[2] and bbox[2] > img_bbox[0] and
                                bbox[1] < img_bbox[3] and bbox[3] > img_bbox[1]):
                            is_suspicious = True
                            reasons.append("image_overlap")
                            results["image_overlaps"].append({
                                "page": page_num + 1,
                                "text": text,
                                "bbox": bbox
                            })
                            break

                    if is_suspicious:
                        result_entry = {
                            "page": page_num + 1,
                            "text": text,
                            "color": color,
                            "size": size,
                            "font": font,
                            "bbox": bbox,
                            "reasons": reasons
                        }
                        results["suspicious_texts"].append(result_entry)

                        if verbose:
                            print(f"SUSPICIOUS [{', '.join(reasons)}]: '{text}' | "
                                  f"Size: {size:.1f} | Color: {color} | Font: {font}")

    doc.close()
    return results


def extract_images(pdf_path, output_dir=None):
    """PDF에서 이미지 추출"""
    doc = fitz.open(pdf_path)

    if output_dir is None:
        output_dir = Path(pdf_path).parent / "extracted_images"
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    extracted = []
    for page_num, page in enumerate(doc):
        image_list = page.get_images(full=True)

        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            filename = f"page_{page_num + 1}_img_{img_idx}.{image_ext}"
            filepath = output_dir / filename

            with open(filepath, "wb") as f:
                f.write(image_bytes)

            extracted.append(str(filepath))
            print(f"Saved: {filepath}")

    doc.close()
    return extracted


def find_hidden_text(pdf_path):
    """흰색/투명 텍스트 찾기"""
    results = analyze_pdf(pdf_path, verbose=False)

    hidden = [t for t in results["suspicious_texts"] if "white_text" in t["reasons"]]

    print(f"\n=== Hidden (White) Texts: {len(hidden)} ===")
    for item in hidden:
        print(f"Page {item['page']}: '{item['text']}'")

    return hidden


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_analyzer.py <pdf_path>")
        print("       python pdf_analyzer.py <pdf_path> --extract-images")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if len(sys.argv) > 2 and sys.argv[2] == "--extract-images":
        extract_images(pdf_path)
    else:
        results = analyze_pdf(pdf_path)
        print(f"\n=== Summary ===")
        print(f"Total pages: {results['total_pages']}")
        print(f"Suspicious texts: {len(results['suspicious_texts'])}")
        print(f"Image overlaps: {len(results['image_overlaps'])}")
