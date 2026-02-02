#!/bin/bash

# docker context 배포를 위한 쉘 스크립트
# 사용법: ./deploy.sh [test|prod]

TARGET=$1

if [ "$TARGET" == "test" ]; then
    echo "테스트 서버 배포"
    docker --context remote-test compose -f docker-compose.test.yml up -d --build
    echo "테스트 서버 배포 완료"

elif [ "$TARGET" == "product" ]; then
    echo "운영 서버 배포"
    # 운영 배포 전 확인 절차 (선택 사항)
    read -p "운영 서버에 배포 진행하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker --context remote-product compose -f docker-compose.product.yml up -d --build
        echo "운영 서버 배포 완료"
    fi

else
    echo "Usage: ./deploy.sh [test|product]"
fi