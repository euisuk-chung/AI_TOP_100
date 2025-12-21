"""
AI 입국 심사관 - 30명 신청자 심사 스크립트 v2
여권 이미지에서 추출한 데이터 포함
"""
import pypdf
import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
INSPECTION_DATE = datetime(2025, 11, 22)

# 영사관 매칭
CONSULATE_MAP = {
    'Republic of Valeria': 'Atlantis Consulate Valeria',
    'Kingdom of Neverland': 'Atlantis Consulate Neverland',
    'Federation of Serenia': 'Atlantis Consulate Serenia',
    'Empire of Dragonia': 'Atlantis Consulate Dragonia',
    'Republic of Crystalline': 'Atlantis Consulate Crystalline',
    'United States of Eldorado': 'Atlantis Consulate Eldorado',
    'Mystical Islands': 'Atlantis Consulate Mystical',
    'Kingdom of Avalon': 'Atlantis Consulate Avalon'
}

# 무비자 협정국 및 허용 기간
# 규칙에 따라 설정 - 비자 없이 입국 가능한 국가들
VISA_FREE_COUNTRIES = {
    'Kingdom of Neverland': 30,
    'Federation of Serenia': 60,
    'Republic of Valeria': 90
}

# 여권 데이터 (이미지에서 추출)
with open(BASE_DIR / 'passport_data.json', 'r') as f:
    PASSPORT_DATA = json.load(f)


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d')
    except:
        return None


def extract_pdf_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        return ''


def parse_visa(text):
    data = {'exists': True}

    name_match = re.search(r'FULL NAME\s*\n?\s*([A-Z][A-Z\s]+?)(?:\n|PASSPORT)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'PASSPORT NUMBER\s*\n?\s*([A-Z0-9]+)', text)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    type_match = re.search(r'VISA TYPE\s*\n?\s*([A-Z]+)', text)
    if type_match:
        data['visa_type'] = type_match.group(1).strip()

    exp_match = re.search(r'EXPIRY DATE\s*\n?\s*(\d{4}-\d{2}-\d{2})', text)
    if exp_match:
        data['expiry_date'] = exp_match.group(1)

    dur_match = re.search(r'DURATION OF STAY\s*\n?\s*(\d+)\s*days?', text)
    if dur_match:
        data['duration'] = int(dur_match.group(1))

    entries_match = re.search(r'ENTRIES ALLOWED\s*\n?\s*(SINGLE|MULTIPLE)', text)
    if entries_match:
        data['entries'] = entries_match.group(1).strip()

    consulate_match = re.search(r'Issued by\s+(Atlantis Consulate \w+)', text)
    if consulate_match:
        data['consulate'] = consulate_match.group(1).strip()

    return data


def parse_arrival_declaration(text):
    data = {'exists': True}

    name_match = re.search(r'Full Name\s*\n?\s*([A-Z][A-Z\s]+?)(?:\n|Passport)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'Passport Number\s*\n?\s*([A-Z0-9]+)', text)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    purpose_match = re.search(r'Purpose of Visit\s*\n?\s*([A-Z]+)', text)
    if purpose_match:
        data['purpose'] = purpose_match.group(1).strip()

    dur_match = re.search(r'Duration of Stay \(days\)\s*\n?\s*(\d+)', text)
    if dur_match:
        data['duration'] = int(dur_match.group(1))

    prev_match = re.search(r'Previous Visits\s*\n?\s*(Yes|No)', text, re.IGNORECASE)
    if prev_match:
        data['previous_visits'] = prev_match.group(1).strip().lower() == 'yes'

    cash_match = re.search(r'Cash Amount Carrying\s*\n?\s*\$?(\d[\d,]*)', text)
    if cash_match:
        data['cash_amount'] = int(cash_match.group(1).replace(',', ''))

    return data


def parse_flight_ticket(text):
    data = {'exists': True}

    name_match = re.search(r'PASSENGER NAME\s*\n?\s*([A-Z][A-Z\s]+?)(?:\n|FROM)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'Passport:\s*([A-Z0-9]+)', text)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    date_match = re.search(r'DATE\s*\n?\s*(\d{4}-\d{2}-\d{2})', text)
    if date_match:
        data['arrival_date'] = date_match.group(1)

    return data


def parse_health_certificate(text):
    data = {'exists': True}

    name_match = re.search(r'(?:Patient Name|Full Name|Name)\s*[:\n]?\s*([A-Z][A-Z\s]+?)(?:\n|Passport|Date|Birth)', text, re.IGNORECASE)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'Passport(?:\s*(?:Number|No\.?))?\s*[:\n]?\s*([A-Z0-9]+)', text, re.IGNORECASE)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    issue_match = re.search(r'(?:Issue Date|Certificate Date|Date of Issue|Examination Date)\s*[:\n]?\s*(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
    if issue_match:
        data['issue_date'] = issue_match.group(1)

    fever_match = re.search(r'Fever\s*[:\n]?\s*(Yes|No)', text, re.IGNORECASE)
    if fever_match:
        data['fever'] = fever_match.group(1).strip().lower() == 'yes'

    covid_match = re.search(r'COVID-?19 Symptoms?\s*[:\n]?\s*(Yes|No)', text, re.IGNORECASE)
    if covid_match:
        data['covid_symptoms'] = covid_match.group(1).strip().lower() == 'yes'

    # Vaccination doses
    doses = len(re.findall(r'(?:1st|2nd|3rd|First|Second|Third|Dose\s*\d)', text, re.IGNORECASE))
    if doses > 0:
        data['vaccination_doses'] = doses
    else:
        vax_match = re.search(r'(?:Number of Doses|Doses)\s*[:\n]?\s*(\d+)', text, re.IGNORECASE)
        if vax_match:
            data['vaccination_doses'] = int(vax_match.group(1))

    return data


def parse_financial_proof(text):
    data = {'exists': True}

    name_match = re.search(r'(?:Account Holder|Name)\s*[:\n]?\s*([A-Z][A-Z\s]+?)(?:\n|Account|Passport)', text, re.IGNORECASE)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'Passport(?:\s*(?:ID|Number|No\.?))?\s*[:\n]?\s*([A-Z0-9]+)', text, re.IGNORECASE)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    date_match = re.search(r'(?:Statement Date|Issue Date|As of)\s*[:\n]?\s*(\d{4}-\d{2}-\d{2})', text, re.IGNORECASE)
    if date_match:
        data['statement_date'] = date_match.group(1)

    balance_match = re.search(r'(?:Available Balance|Balance)\s*[:\n]?\s*\$?([\d,]+(?:\.\d{2})?)', text, re.IGNORECASE)
    if balance_match:
        data['balance'] = float(balance_match.group(1).replace(',', ''))

    return data


def parse_customs_declaration(text):
    data = {'exists': True}

    name_match = re.search(r'(?:Full Name|Name)\s*[:\n]?\s*([A-Z][A-Z\s]+?)(?:\n|Passport)', text, re.IGNORECASE)
    if name_match:
        data['name'] = name_match.group(1).strip()

    passport_match = re.search(r'Passport(?:\s*(?:Number|No\.?))?\s*[:\n]?\s*([A-Z0-9]+)', text, re.IGNORECASE)
    if passport_match:
        data['passport_no'] = passport_match.group(1).strip()

    prohibited_match = re.search(r'[Pp]rohibited items?\s*[:\?]?\s*(YES|NO)', text, re.IGNORECASE)
    if prohibited_match:
        data['prohibited_items'] = prohibited_match.group(1).strip().upper() == 'YES'

    restricted_match = re.search(r'[Rr]estricted items?\s*[:\?]?\s*(YES|NO)', text, re.IGNORECASE)
    if restricted_match:
        data['restricted_items'] = restricted_match.group(1).strip().upper() == 'YES'

    value_match = re.search(r'(?:Total Value|Declared Value)\s*[:\n]?\s*\$?([\d,]+)', text, re.IGNORECASE)
    if value_match:
        data['declared_value'] = int(value_match.group(1).replace(',', ''))

    food_match = re.search(r'(?:Food|Animal|Plant)\s*(?:products?)?\s*[:\?]?\s*(YES|NO)', text, re.IGNORECASE)
    if food_match:
        data['food_products'] = food_match.group(1).strip().upper() == 'YES'

    return data


def load_applicant_data(app_id, base_path):
    app_path = os.path.join(base_path, app_id)
    files = [f for f in os.listdir(app_path) if f.endswith('.pdf')]

    data = {
        'id': app_id,
        'passport': None,
        'visa': None,
        'arrival': None,
        'flight': None,
        'health': None,
        'financial': None,
        'customs': None
    }

    # 여권 데이터는 이미지에서 추출한 데이터 사용
    passport_data = PASSPORT_DATA.get(app_id)
    if passport_data:
        data['passport'] = {
            'exists': True,
            'name': passport_data['name'],
            'passport_no': passport_data['passport_no'],
            'nationality': passport_data['nationality'],
            'expiry_date': passport_data['expiry_date'],
            'has_photo': True
        }

    for f in files:
        fpath = os.path.join(app_path, f)
        text = extract_pdf_text(fpath)

        if 'visa' in f:
            data['visa'] = parse_visa(text)
        elif 'arrival_declaration' in f:
            data['arrival'] = parse_arrival_declaration(text)
        elif 'flight_ticket' in f:
            data['flight'] = parse_flight_ticket(text)
        elif 'health_certificate' in f:
            data['health'] = parse_health_certificate(text)
        elif 'financial_proof' in f:
            data['financial'] = parse_financial_proof(text)
        elif 'customs_declaration' in f:
            data['customs'] = parse_customs_declaration(text)

    return data


def check_rules(data):
    """Check all 25 rules and return (result, reason)"""
    violations = []

    passport = data.get('passport')
    visa = data.get('visa')
    arrival = data.get('arrival')
    flight = data.get('flight')
    health = data.get('health')
    financial = data.get('financial')
    customs = data.get('customs')

    # Rule 1: 여권 미제출
    if not passport:
        violations.append(1)
        return ('Deny', min(violations))

    nationality = passport.get('nationality', '') if passport else ''
    purpose = arrival.get('purpose', '') if arrival else ''
    duration = arrival.get('duration', 0) if arrival else 0

    # Rule 2: 비자 미제출 (무비자 협정국 예외)
    if not visa:
        if purpose == 'STUDY':
            violations.append(2)
        elif nationality not in VISA_FREE_COUNTRIES:
            violations.append(2)

    # Rule 3: 입국신고서 미제출
    if not arrival:
        violations.append(3)

    # Rule 4: 항공권 미제출
    if not flight:
        violations.append(4)

    # Rule 5: 재정증명서 미제출 (조건부)
    needs_financial = False
    if purpose == 'TOURISM' and duration >= 14:
        needs_financial = True
    if purpose == 'BUSINESS' and duration >= 30:
        needs_financial = True
    if purpose == 'STUDY':
        needs_financial = True

    if needs_financial and not financial:
        violations.append(5)

    # Rule 6: 건강증명서 미제출
    if not health:
        violations.append(6)

    # Rule 7: 세관신고서 미제출 (조건부)
    cash_amount = arrival.get('cash_amount', 0) if arrival else 0
    declared_value = customs.get('declared_value', 0) if customs else 0
    food_products = customs.get('food_products', False) if customs else False

    needs_customs = False
    if cash_amount >= 10000:
        needs_customs = True

    if needs_customs and not customs:
        violations.append(7)

    # Rule 8: 이름 불일치 (대소문자 무시, 공백 정규화)
    if passport:
        passport_name = passport.get('name', '').upper().strip()
        docs_to_check = []
        if visa:
            docs_to_check.append(('visa', visa.get('name', '')))
        if arrival:
            docs_to_check.append(('arrival', arrival.get('name', '')))
        if flight:
            docs_to_check.append(('flight', flight.get('name', '')))
        if health:
            docs_to_check.append(('health', health.get('name', '')))
        if financial:
            docs_to_check.append(('financial', financial.get('name', '')))
        if customs:
            docs_to_check.append(('customs', customs.get('name', '')))

        for doc_name, name in docs_to_check:
            if name:
                norm_name = name.upper().strip()
                if norm_name != passport_name:
                    violations.append(8)
                    break

    # Rule 9: 여권번호 불일치
    if passport:
        passport_no = passport.get('passport_no', '')
        docs_to_check = []
        if visa:
            docs_to_check.append(('visa', visa.get('passport_no', '')))
        if arrival:
            docs_to_check.append(('arrival', arrival.get('passport_no', '')))
        if flight:
            docs_to_check.append(('flight', flight.get('passport_no', '')))
        if health:
            docs_to_check.append(('health', health.get('passport_no', '')))
        if financial:
            docs_to_check.append(('financial', financial.get('passport_no', '')))
        if customs:
            docs_to_check.append(('customs', customs.get('passport_no', '')))

        for doc_name, pno in docs_to_check:
            if pno and pno != passport_no:
                violations.append(9)
                break

    # Rule 10: 여권 만료
    if passport:
        exp_date = parse_date(passport.get('expiry_date', ''))
        if exp_date and exp_date < INSPECTION_DATE:
            violations.append(10)

    # Rule 11: 비자 만료
    if visa:
        exp_date = parse_date(visa.get('expiry_date', ''))
        if exp_date and exp_date < INSPECTION_DATE:
            violations.append(11)

    # Rule 12: 건강증명서 기간 초과 (14일)
    if health:
        issue_date = parse_date(health.get('issue_date', ''))
        if issue_date and (INSPECTION_DATE - issue_date).days > 14:
            violations.append(12)

    # Rule 13: 항공권 날짜 불일치
    if flight:
        arrival_date = parse_date(flight.get('arrival_date', ''))
        if arrival_date and arrival_date.date() != INSPECTION_DATE.date():
            violations.append(13)

    # Rule 14: 재정증명서 발급일 초과 (30일)
    if financial:
        stmt_date = parse_date(financial.get('statement_date', ''))
        if stmt_date and (INSPECTION_DATE - stmt_date).days > 30:
            violations.append(14)

    # Rule 15: 여권 사진 미부착
    if passport and not passport.get('has_photo', True):
        violations.append(15)

    # Rule 16: 무효한 입국 목적
    if arrival:
        valid_purposes = ['TOURISM', 'BUSINESS', 'STUDY']
        if purpose not in valid_purposes:
            violations.append(16)

    # Rule 17: 부적절한 비자 타입
    if visa and arrival:
        visa_type = visa.get('visa_type', '')
        purpose = arrival.get('purpose', '')
        expected_visa = {'TOURISM': 'TOURIST', 'BUSINESS': 'BUSINESS', 'STUDY': 'STUDENT'}
        if expected_visa.get(purpose, '') != visa_type:
            violations.append(17)

    # Rule 18: 체류기간 초과
    if arrival:
        req_duration = arrival.get('duration', 0)
        if visa:
            allowed_duration = visa.get('duration', 0)
            if req_duration > allowed_duration:
                violations.append(18)
        elif nationality in VISA_FREE_COUNTRIES:
            allowed_duration = VISA_FREE_COUNTRIES[nationality]
            if req_duration > allowed_duration:
                violations.append(18)

    # Rule 19: 입국 횟수 제한 위반
    if visa and arrival:
        entries = visa.get('entries', '')
        prev_visits = arrival.get('previous_visits', False)
        if entries == 'SINGLE' and prev_visits:
            violations.append(19)

    # Rule 20: 비자 발급지 불일치
    if visa and passport:
        nationality = passport.get('nationality', '')
        consulate = visa.get('consulate', '')
        expected_consulate = CONSULATE_MAP.get(nationality, '')
        if expected_consulate and consulate and consulate != expected_consulate:
            violations.append(20)

    # Rule 21: 발열 증상 보유
    if health and health.get('fever', False):
        violations.append(21)

    # Rule 22: 기타 증상 보유 (COVID-19)
    if health and health.get('covid_symptoms', False):
        violations.append(22)

    # Rule 23: 재정능력 부족
    if financial and arrival:
        balance = financial.get('balance', 0)
        req_duration = arrival.get('duration', 0)
        min_required = req_duration * 100
        if balance < min_required:
            violations.append(23)

    # Rule 24: 백신 접종 미완료 (2회 이상 필수)
    if health:
        doses = health.get('vaccination_doses', 0)
        if doses < 2:
            violations.append(24)

    # Rule 25: 금지품목 소지
    if customs:
        if customs.get('prohibited_items', False) or customs.get('restricted_items', False):
            violations.append(25)

    # Return result
    if violations:
        return ('Deny', min(violations))
    else:
        return ('Approve', None)


def main():
    base_path = str(BASE_DIR / 'applicants')
    applicants = sorted([d for d in os.listdir(base_path) if d.startswith('applicant_')])

    results = []
    details = []

    for app_id in applicants:
        data = load_applicant_data(app_id, base_path)
        answer, reason = check_rules(data)

        result = {'id': app_id, 'answer': answer}
        if reason:
            result['reason'] = reason
        results.append(result)

        # 상세 정보
        detail = {
            'id': app_id,
            'answer': answer,
            'reason': reason,
            'passport_name': data['passport'].get('name') if data['passport'] else None,
            'passport_nationality': data['passport'].get('nationality') if data['passport'] else None,
            'arrival_name': data['arrival'].get('name') if data['arrival'] else None,
            'visa_exists': data['visa'] is not None,
            'health_exists': data['health'] is not None
        }
        details.append(detail)

        status = f"Rule {reason}" if reason else "OK"
        print(f"{app_id}: {answer} ({status})")

    # Save results
    with open(BASE_DIR / 'results_v2.json', 'w') as f:
        json.dump(results, f, indent=2)

    with open(BASE_DIR / 'details_v2.json', 'w') as f:
        json.dump(details, f, indent=2, ensure_ascii=False)

    print(f"\nTotal: {len(results)} applicants processed")
    approved = sum(1 for r in results if r['answer'] == 'Approve')
    denied = sum(1 for r in results if r['answer'] == 'Deny')
    print(f"Approved: {approved}")
    print(f"Denied: {denied}")

    # 거절 사유별 통계
    print("\n=== 거절 사유 통계 ===")
    reason_counts = {}
    for r in results:
        if r['answer'] == 'Deny':
            reason = r.get('reason', 0)
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    for reason, count in sorted(reason_counts.items()):
        print(f"Rule {reason}: {count}명")


if __name__ == "__main__":
    main()
