from pydantic import BaseModel, Field

# 기본정보
class userBaseData(BaseModel):
    age: int = Field(description="신청자 나이")
    sex: str = Field(description="신청자 성별(남자,여자)")
    wealth: str = Field(description="신청자 순자산")
    income: str = Field(description="신청자 소득")

# 설문 결과
class assetData(BaseModel):
    base: userBaseData = Field(description="신청자 기초정보")
    answers: list[list[int]] = Field(description="신청자 설문항목")
    etc: str = Field(description="기타 하고 싶은 말")

# 자산 리스트
class assetItem(BaseModel):
    asset_name: str = Field(description="상품명 (예: S&P 500 ETF, TDF 2050 등)")
    weight: int = Field(description="자산별 비중 (%)")

# 포트폴리오 결과
class portfolioResult(BaseModel):
    summary: str = Field(description="투자 성향 분석 및 핵심 요약을 담은 마크다운 텍스트")
    chart_data: list[assetItem] = Field(description="차트 렌더링을 위한 자산명과 비중 리스트")
    table_content: str = Field(description="포트폴리오에 편입된 상품 리스트, 추천 사유, 기대 역할을 정리한 마크다운 표(Table)")
    advice: str = Field(description="매니저의 실전 조언을 담은 마크다운 불릿 리스트")