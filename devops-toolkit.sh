#!/bin/bash

##This is a script to check day to day activity for devops#
#save it and use in ur machine#



clear

# Colors
GREEN='\033[0;32m'
BLUE='\033[1;34m'
RED='\033[0;31m'
NC='\033[0m'

dashboard() {

echo ""
echo "========================================="
echo "        DEVOPS DASHBOARD"
echo "========================================="

############################
# Kubernetes
############################

echo ""
echo "========== Kubernetes =========="
kubectl get nodes
echo ""

############################
# Calculator App
############################

echo "========== Calculator App =========="
echo "Deployment:"
kubectl get deploy

echo ""
echo "Pods:"
kubectl get pods

echo ""
echo "Service:"
kubectl get svc

echo ""
echo "Open Calculator:"
echo "minikube service calculator-service"
echo ""

############################
# ArgoCD
############################

echo "========== ArgoCD =========="

if kubectl get ns argocd >/dev/null 2>&1; then

echo "Username : admin"

echo -n "Password : "
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" 2>/dev/null | base64 -d
echo ""

echo ""
echo "Open Dashboard:"
echo "kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo "https://localhost:8080"

fi

############################
# Grafana
############################

echo ""
echo "========== Grafana =========="

if kubectl -n monitoring get secret monitoring-grafana >/dev/null 2>&1; then

echo "Username : admin"

echo -n "Password : "
kubectl -n monitoring get secret monitoring-grafana \
-o jsonpath="{.data.admin-password}" | base64 -d
echo ""

echo ""
echo "Open Dashboard:"
echo "kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80"
echo "http://localhost:3000"

fi

############################
# Prometheus
############################

echo ""
echo "========== Prometheus =========="

if kubectl -n monitoring get svc monitoring-kube-prometheus-prometheus >/dev/null 2>&1; then

echo "Open Dashboard:"
echo "kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090"
echo "http://localhost:9090"

fi

############################
# Kubernetes Dashboard
############################

echo ""
echo "========== Kubernetes Dashboard =========="
echo "Run:"
echo "minikube dashboard"

echo ""

}

cluster() {

echo ""
echo "========== Cluster =========="
kubectl get nodes
kubectl get pods -A
kubectl top nodes
echo ""

}

application() {

echo ""
echo "========== Calculator =========="

kubectl get deploy
echo ""

kubectl get pods
echo ""

kubectl get svc
echo ""

kubectl top pods
echo ""

}

logs() {

echo ""
kubectl logs deployment/calculator-app --tail=20
echo ""

}

restart_app() {

echo ""
kubectl rollout restart deployment calculator-app
echo ""

}

scale_app() {

read -p "Enter replicas: " replicas

kubectl scale deployment calculator-app --replicas=$replicas

echo ""

kubectl get pods

}

docker_info() {

echo ""
echo "========== Docker =========="

docker image ls

echo ""

docker ps

echo ""

docker system df

}

helm_info() {

echo ""
echo "========== Helm =========="

helm list -A

}

argocd_info() {

echo ""
kubectl get application -n argocd

}

system_info() {

echo ""
echo "========== Memory =========="
free -h

echo ""
echo "========== Disk =========="
df -h

echo ""
echo "========== CPU =========="
nproc

}

while true
do

echo ""
echo -e "${BLUE}==============================${NC}"
echo -e "${GREEN} DEVOPS ENGINEER TOOLKIT ${NC}"
echo -e "${BLUE}==============================${NC}"

echo "1) Dashboard"
echo "2) Cluster Status"
echo "3) Calculator Application"
echo "4) Restart Application"
echo "5) Scale Application"
echo "6) Application Logs"
echo "7) Docker"
echo "8) Helm"
echo "9) ArgoCD"
echo "10) System Info"
echo "11) Exit"

echo ""

read -p "Select option: " choice

case $choice in

1)
dashboard
;;

2)
cluster
;;

3)
application
;;

4)
restart_app
;;

5)
scale_app
;;

6)
logs
;;

7)
docker_info
;;

8)
helm_info
;;

9)
argocd_info
;;

10)
system_info
;;

11)
echo "Bye 👋"
exit
;;

*)
echo "Invalid Option"
;;

esac

done
