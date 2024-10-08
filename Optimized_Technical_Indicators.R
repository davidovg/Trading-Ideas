
#data<-read.csv("E://d/DAX_01_08_2012_10mins.csv", header=TRUE, sep=";")
#data<-read.csv("E://d/sp_11_03_2009.csv", header=TRUE, sep=";")
data<-read.csv("E://programming/Projects/GDAXI_26_06_2015_Hourly.csv", header=TRUE, sep=",")
#data<-read.csv("E://d/gold_09_08_2012-1000hourly.csv", header=TRUE, sep=";")
#data<-read.csv("E://d/gold_01_09_2008-1000hourly.csv", header=TRUE, sep=";")

#data<-read.csv("E://d/sp_01_09_2008-2000hourly.csv", header=TRUE, sep=";")

date <- data[,1]
volume <- data[,8]
open <- data[,4]
close <- data[,7]
min <- data[,6]
max <- data[,5]


sr_ar <- function(j, i) { # simple moving average i and j-th combination 
  s <- 0
  for (k in 0:(j-1)) {
    s <- (s + open[i-k])}
  s <- s/j
  return(s) }


sr_ar_pr <- function(j, i) { # moving weighted average for i-th and j-th combination
  s <- 0; t <- 0
  for (k in 0:(j-1)) {
    s <- s + open[i-k]*(j-k)
    t <- t + j - k}
  s <- s/t
  return(s)}


sr_ar_exp <- function(j, i) { # exponential moving average i and j-th coeff.
  ko <- 2/(j + 1)
  s <- sr_ar(j, j)
  for (k in (j+1):i) {
    s <- ko*open[k] + (1-ko)*s }
  return(s) }


rfi <- function(i) { # computing the pure force index
  r <- volume[i]*(close[i]-close[i-1])
  return(r)}


fi <- function(i, j) { # computing the force index with period of averaging j 
  s <- 0
  for (k in (i-j+1):j) {
    s <- s+rfi(k)}
  s <- s/j
  return(s)}



rsi <- function(j, i) { # computing RSI for i-th observation backwards to the j-th one
  u <- 0
  d <- 0
  k <- 0
  while (k < j) {
    if (open[i-k] > open[i-k-1]) { # when the price goes up 
      u <- u + open[i-k]}
    if (open[i-k] < open[i-k-1]) { # when the price goes down
      d <- d + open[i-k]}     
    k <- k+1}
  r <- 100*(1-d/(d+u))
  return(r)}


an <- function(j, i) {  # ������ ����������� �� ������� �� i-�� ���� �� �� 2 �� j ��. ����������
  a <- c()
  for (k in 2:j) a <- c(a, sr_ar(k, i))
  b <- sort(a)
  c <- c()
  for (l in 1:(j-1)) {
    k <- 1
    while(a[l]!=b[k])
      k <- k+1
    c <- c(c, k)}
  return(c) }

eq <- function(x, y) { # ��������� ���� ����������� ������� x � y ��������
  lx <- length(x)
  z <- TRUE
  for (j in 1:lx) {
    if (x[j] != y[j]) {z <- FALSE; j <- lx+5}}
  return(z)}


cci <- function(i, j) { # �������� cci �� i-�� ���� � j-�� ���������� �����
  tp <- c()
  for (k in (i-j+1):i) {
    tp <- c(tp, (min[k]+max[k]+close[k])/3) }
  tpi <- tp[j]
  sma <- sum(tp)/j
  for (k in 1: j) {
    tp[k] <- abs(tp[k]-sma) }
  d <- sum(tp)/j
  ci <- (tpi-sma)/(0.015*d)
  return(ci) }


hod_cci <- function(i, j, sum, akc) { # ����� cci �� i-�� ���� j-�� ����������
  if ((cci(i-1, j) > 100) & (cci(i-1, j) > cci(i, j))) { # ������� �� ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  if ((cci(i-1, j) < -100) & (cci(i-1, j) < cci(i, j))) { # ������� �� ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }


optim_cci <- function(i, j) { # ����� cci �� i-�� ���� j-�� ����������
  r <- "Do not enter a position"
  if ((cci(i-1, j) > 100) & (cci(i-1, j) > cci(i, j))) { # ������� �� ���������
    r <- "Sell" }
  if ((cci(i-1, j) < -100) & (cci(i-1, j) < cci(i, j))) { # ������� �� ��������
    r <- "Buy" }
  return(r) }



hod_fi <- function(i, j, sum, akc) { # ����� rf �� i-�� ���� j-�� ����������
  if ((fi(i-1, j) > 0) & (fi(i, j) > 0) & (fi(i-1, j) > fi(i, j))) { # ������� �� ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  if ((fi(i-1, j) < 0) & (fi(i, j) < 0) & (fi(i-1, j) < fi(i, j))) { # ������� �� ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }


optim_fi <- function(i, j) { # ����� fi �� i-�� ���� j-�� ����������
  r <- "Do not enter a position"
  if ((fi(i-1, j) > 0) & (fi(i, j) > 0) & (fi(i-1, j) > fi(i, j))) { # ������� �� ���������
    r <- "Sell" }
  if ((fi(i-1, j) < 0) & (fi(i, j) < 0) & (fi(i-1, j) < fi(i, j))) { # ������� �� ��������
    r <- "Buy" }
  return(r) }




hod_alig1 <-function(i, sum, akc) { # ����� �� ��������� �� i-�� ���� ����������� ��.�����.
  al13 <- sr_ar(13, i-8); al13_ <- sr_ar(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar(8, i-5); al8_ <- sr_ar(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar(5, i-3); al5_ <- sr_ar(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))              # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))         # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))              # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))         # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                  # ������� �� ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  if (t2 & t2_ & (al13 > al13_)) {                # ������� �� ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }


optim_alig1 <-function(i) { # ����� �� ��������� �� i-�� ���� ����������� ��.�����.
  r <- "Do not enter a position"
  al13 <- sr_ar(13, i-8); al13_ <- sr_ar(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar(8, i-5); al8_ <- sr_ar(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar(5, i-3); al5_ <- sr_ar(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))              # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))         # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))              # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))         # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                  # ������� �� ��������
    r <- "Buy" }
  if (t2 & t2_ & (al13 > al13_)) {                # ������� �� ���������
    r <- "Sell" }
  return(r) }



hod_alig2 <-function(i, sum, akc) { # ����� �� ��������� �� i-�� ���� ��.�����. ����������
  r <- "Do not enter a position"
  al13 <- sr_ar_pr(13, i-8); al13_ <- sr_ar_pr(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar_pr(8, i-5); al8_ <- sr_ar_pr(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar_pr(5, i-3); al5_ <- sr_ar_pr(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))                    # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))               # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))                    # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))               # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                        # ������� �� ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  if (t2 & t2_ & (al13 > al13_)) {                      # ������� �� ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }



optim_alig2 <-function(i) { # ����� �� ��������� �� i-�� ���� ��.�����. ����������
  r <- "Do not enter a position"
  al13 <- sr_ar_pr(13, i-8); al13_ <- sr_ar_pr(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar_pr(8, i-5); al8_ <- sr_ar_pr(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar_pr(5, i-3); al5_ <- sr_ar_pr(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))                    # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))               # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))                    # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))               # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                        # ������� �� ��������
    r <- "Buy" } 
  if (t2 & t2_ & (al13 > al13_)) {                      # ������� �� ���������
    r <- "Sell" }
  return(r) }

hod_alig3 <-function(i, sum, akc) { # ����� �� ��������� �� i-�� ���� ��.�����. ��������������
  al13 <- sr_ar_exp(13, i-8); al13_ <- sr_ar_exp(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar_exp(8, i-5); al8_ <- sr_ar_exp(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar_exp(5, i-3); al5_ <- sr_ar_exp(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))                    # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))               # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))                    # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))               # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                        # ������� �� ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  if (t2 & t2_ & (al13 > al13_)) {                      # ������� �� ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }


optim_alig3 <-function(i) { # ����� �� ��������� �� i-�� ���� ��.�����. ��������������
  r <- "Do not enter a position"
  al13 <- sr_ar_exp(13, i-8); al13_ <- sr_ar_exp(13, i-9) # ��� �������������� ���� �����
  al8 <- sr_ar_exp(8, i-5); al8_ <- sr_ar_exp(8, i-6)     # ��� �������������� ������� �����
  al5 <- sr_ar_exp(5, i-3); al5_ <- sr_ar_exp(5, i-4)     # ��� �������������� ������ �����
  t1 <- ((al5 > al8) & (al8 > al13))                    # ��������� ��� i-�� ���� ������, �������, �����
  t1_ <- ((al5_ > al8_) & (al8_ > al13_))               # ���������� i-1-�� ����
  t2 <- ((al5 < al8) & (al8 < al13))                    # ��������� ��� i-�� ���� �����, �������, ������
  t2_ <- ((al5_ < al8_) & (al8_ < al13_))               # ���������� i-1-�� ����
  if (t1 & t1_ & (al5 > al5_)) {                        # ������� �� ��������
    r <- "Buy" } 
  if (t2 & t2_ & (al13 > al13_)) {                      # ������� �� ���������
    r <- "Sell" }
  return(r) }



k_sholast <- function(i, j) { # �������� k-�������. ��������� �� i-�� ���� � j ��������� ����
  a <- c()
  for (n in (i-j):(i)) a <- c(a, open[n])
  l <- min(a) # ����������� �������� � ��������� � ������� j
  h <- max(a) # ������������ �������� � ��������� � ������� j
  c <- open[i]
  k <- (c-l)/(h-l)*100
  return(k)}

hod_sholast1 <- function(i, j, sum, akc) { # ��� �������.��������� �� i-�� ����, j ��������� ����
  ks <- 0
  for (n in (j+1):(i-1)) { # ����� �� ���������� �� ������ ��������� �� k �� i-1���� ����
    ks <- ks+k_sholast(n, j)}
  d_ <- ks/(i-j-1) # i-1 ���� �������� �� d
  k_ <- k_sholast((i-1), j) # i-1 ���� �������� �� k
  k <- k_sholast(i, j) # i �� �������� �� k
  d <- (ks+k_)/(i-j) # i �� �������� �� d
  if ((k_ < d_) & (k > d)) { # k ������� d ������ - ������
    m <- sum %/% open[i]
    sum <- sum - m*open[i]
    akc <- akc + m }
  if ((k_ > d_) & (k < d)) { # k ������� d ������ - �������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }

optim_sholast1 <- function(i, j) { # ��� �������.��������� �� i-�� ����, j ��������� ����
  r <- "Do not enter a position"
  ks <- 0
  for (n in (j+1):(i-1)) { # ����� �� ���������� �� ������ ��������� �� k �� i-1���� ����
    ks <- ks+k_sholast(n, j)}
  d_ <- ks/(i-j-1) # i-1 ���� �������� �� d
  k_ <- k_sholast((i-1), j) # i-1 ���� �������� �� k
  k <- k_sholast(i, j) # i �� �������� �� k
  d <- (ks+k_)/(i-j) # i �� �������� �� d
  if ((k_ < d_) & (k > d)) { # k ������� d ������ - ������
    r <- "Buy"}
  if ((k_ > d_) & (k < d)) { # k ������� d ������ - �������
    r <- "Sell" }
  return(r) }




hod_sholast2 <- function(i, j, sum, akc) { # ��� �������.��������� �� i-�� ����, j ��������� ����
  k_ <- k_sholast((i-1), j) # i-1 ���� �������� �� k
  k <- k_sholast(i, j) # i �� �������� �� k
  if ((k_ < 20) & (k_ < k)) { # k � ��������� ������� ������� ��-����� �� 20 - ������
    m <- sum %/% open[i]
    sum <- sum - m*open[i]
    akc <- akc + m }
  if ((k_ > 80) & (k_ > k)) { # k � ��������� ������� �������� ��-����� �� 80 - �������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }


optim_sholast2 <- function(i, j) { # ��� �������.��������� �� i-�� ����, j ��������� ����
  r <- "Do not enter a position"
  k_ <- k_sholast((i-1), j) # i-1 ���� �������� �� k
  k <- k_sholast(i, j) # i �� �������� �� k
  if ((k_ < 20) & (k_ < k)) { # k � ��������� ������� ������� ��-����� �� 20 - ������
    r <- "Buy" }
  if ((k_ > 80) & (k_ > k)) { # k � ��������� ������� �������� ��-����� �� 80 - �������
    r <- "Sell" }
  return(r) }


hod_extr <- function(i, j, sum, akc) { # ������ ��������� �� ���������� �� i-�� ���� �� j ��������� �����
  a <- c()
  for (k in (i-j-1):(i-1)) a <- c(a, open[k])
  amax <- max(a)  # ������������ ���� �� ����������� j ���� 
  amin <- min(a)  # ����������� ���� �� ����������� j ����
  if (amax < open[i]) {               # ��� ������� ���� ��-������ - ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  if (amin > open[i]) {
    l <- sum %/% open[i]
    sum <- sum - l*open[i]         # ��� ������� ���� ��-����� - ��������
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }


optim_extr <- function(i, j) { # ������ ��������� �� ���������� �� i-�� ���� �� j ��������� �����
  r <- "Do not enter a position"
  a <- c()
  for (k in (i-j-1):(i-1)) a <- c(a, open[k])
  amax <- max(a)  # ������������ ���� �� ����������� j ���� 
  amin <- min(a)  # ����������� ���� �� ����������� j ����
  if (amax < open[i]) {               # ��� ������� ���� ��-������ - ���������
    r <- "Sell" }
  if (amin > open[i]) {
    r <- "Buy" }
  return(r) }




hod_srar <- function(i, j, k, sum, akc) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.�����������
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  if ((sr_ar(j,(i-1)) - sr_ar(k, (i-1)) < 0) & ((sr_ar(j,i) - sr_ar(k, i) >= 0))) { # ��� ������� ������ - ���������
    sum <- sum + akc * open[i]
    akc <- 0 } 
  if ((sr_ar(j,(i-1)) - sr_ar(k, (i-1)) > 0) & ((sr_ar(j,i) - sr_ar(k, i) <= 0))) { # ��� ������� ������ - ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }


optim_srar <- function(i, j, k)    {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.�����������
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  r <- "Do not enter a position"
  if ((sr_ar(j,(i-1)) - sr_ar(k, (i-1)) < 0) & ((sr_ar(j,i) - sr_ar(k, i) >= 0))) { # ��� ������� ������ - ���������
    r <- "Sell" } 
  if ((sr_ar(j,(i-1)) - sr_ar(k, (i-1)) > 0) & ((sr_ar(j,i) - sr_ar(k, i) <= 0))) { # ��� ������� ������ - ��������
    r <- "Buy" }
  return(r) }




hod_srar_pr <- function(i, j, k, sum, akc) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.����������� ����������
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  if ((sr_ar_pr(j,(i-1)) - sr_ar_pr(k, (i-1)) < 0) & ((sr_ar_pr(j,i) - sr_ar_pr(k, i) >= 0))) { # ��� ������� ������ - ���������
    sum <- sum + akc * open[i]
    akc <- 0 } 
  if ((sr_ar_pr(j,(i-1)) - sr_ar_pr(k, (i-1)) > 0) & ((sr_ar_pr(j,i) - sr_ar_pr(k, i) <= 0))) { # ��� ������� ������ - ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }

optim_srar_pr <- function(i, j, k) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.����������� ����������
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  r <- "Do not enter a position"
  if ((sr_ar_pr(j,(i-1)) - sr_ar_pr(k, (i-1)) < 0) & ((sr_ar_pr(j,i) - sr_ar_pr(k, i) >= 0))) { # ��� ������� ������ - ���������
    r <- "Sell"} 
  if ((sr_ar_pr(j,(i-1)) - sr_ar_pr(k, (i-1)) > 0) & ((sr_ar_pr(j,i) - sr_ar_pr(k, i) <= 0))) { # ��� ������� ������ - ��������
    r <- "Buy" }
  return(r) }




hod_srar_exp <- function(i, j, k, sum, akc) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.����������� ����.
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  if ((sr_ar_exp(j,(i-1)) - sr_ar_exp(k, (i-1)) < 0) & ((sr_ar_exp(j,i) - sr_ar_exp(k, i) >= 0))) { # ��� ������� ������ - ���������
    sum <- sum + akc * open[i]
    akc <- 0 } 
  if ((sr_ar_exp(j,(i-1)) - sr_ar_exp(k, (i-1)) > 0) & ((sr_ar_exp(j,i) - sr_ar_exp(k, i) <= 0))) { # ��� ������� ������ - ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }

optim_srar_exp <- function(i, j, k) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.����������� ����.
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  r <- "Do not enter a position"
  if ((sr_ar_exp(j,(i-1)) - sr_ar_exp(k, (i-1)) < 0) & ((sr_ar_exp(j,i) - sr_ar_exp(k, i) >= 0))) { # ��� ������� ������ - ���������
    r <- "Sell" } 
  if ((sr_ar_exp(j,(i-1)) - sr_ar_exp(k, (i-1)) > 0) & ((sr_ar_exp(j,i) - sr_ar_exp(k, i) <= 0))) { # ��� ������� ������ - ��������
    r <- "Buy" }
  return(r) }




hod_rsi <- function(i, j, sum, akc) {# ������ ��������� �� ���������� �� i-�� ����
  # j-�� � k-�� ��.�����������
  # � ������� ���� sum � ������� ���� ����� akc
  # ��������� � ������ �� ������ ���� � ����� ��. �����
  if (rsi(j,i) > 70) { # ���������
    sum <- sum + akc * open[i]
    akc <- 0 } 
  if (rsi(j,i) <  30) { # ��������
    l <- sum %/% open[i]
    sum <- sum - l*open[i]
    akc <- akc + l }
  r <- c(sum, akc)
  return(r) }


optim_rsi <- function(i, j) {# �������� �������� �� ������ �� rsi 
  # �� i-�� ���� j �����
  r <- "Do not enter a position"                          
  if (rsi(j,i) > 70) {      # ���������
    r <- "Sell" } 
  if (rsi(j,i) <  30) { # ��������
    r <- "Buy"}
  return(r) }




r_wpr <- function(i, j) { # �������� Williams` Percent Range �� i-�� ���� � j ��������� ����
  a <- c()
  for (n in (i-j):(i)) a <- c(a, close[n])
  l <- min(a) # ����������� �������� � ��������� � ������� j
  h <- max(a) # ������������ �������� � ��������� � ������� j
  c <- close[i]
  r <- (h-c)/(h-l)*100
  return(r)}


hod_wpr <- function(i, j, sum, akc) { # ��� Williams` Percent Range �� i-�� ���� � j ��������� ����
  r1 <- r_wpr(i-1, j) 
  r2 <- r_wpr(i, j)   # ��� �������������� ���������
  if ((r1 > 80) & (r2 > 80) & (r1 > r2)) { # ������������� � �������� �� ����������� - ��������
    m <- sum %/% open[i]
    sum <- sum - m*open[i]
    akc <- akc + m }
  if ((r1 < 20) & (r2 < 20) & (r1 < r2)) { # ������������ � �������� �� ����������� - ���������
    sum <- sum + akc * open[i]
    akc <- 0 }
  r <- c(sum, akc)
  return(r) }


optim_wpr <- function(i, j) { # ��� Williams` Percent Range �� i-�� ���� � j ��������� ����
  r <- "Do not enter a position"
  r1 <- r_wpr(i-1, j) 
  r2 <- r_wpr(i, j)   # ��� �������������� ���������
  if ((r1 > 80) & (r2 > 80) & (r1 > r2)) { # ������������� � �������� �� ����������� - ��������
    r <- "Buy" }
  if ((r1 < 20) & (r2 < 20) & (r1 < r2)) { # ������������ � �������� �� ����������� - ���������
    r <- "Sell" }
  return(r) }



ndata <- length(data[,1])


# ������ ���������� ������� �� ������ �� ������������
#-------------------------------------------------------------------------
gra_extrem <- c()
for (j in 3:30) { # ������ ��������� �� ������ ���������� � ������� �� 10 �� 30
  suma <- 100000 # ������� ����
  akcii <- 0 # ������� ���� �����
  for (i in (j+2):ndata) { # ������, ���������� �����������
    r <- hod_extr(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  gra_extrem <- c(gra_extrem, rezult, j)}
for (i in 1:length(gra_extrem)) { # ����� �� ��������� �� ����������� ��������
  if (gra_extrem[i] == max(gra_extrem)) {
    nsr_extrem <- gra_extrem[i+1]
    i <- length(gra_extrem)+10 }}
extr_ <- c(nsr_extrem, max(gra_extrem))
print(max(gra_extrem)); print(nsr_extrem)

# ������ ���������� ������� �� ������ ������ �����������
#-------------------------------------------------------------------------
gra <- c() 
for (k in 2:24) { # ��������� �� ������ ������ ����������� �� ������ ������ 2-25
  for (j in (k+1):25) { # ��������� ������ �� ����� ������ ��.����������� k,k+1 k,k+2 ... k,j
    suma <- 100000 # ������� ����
    akcii <- 0 # ������� ���� �����
    for (i in 30:ndata) { # ������, ���������� �����������
      r <- hod_srar(i, j, k, suma, akcii)
      suma <- r[1]
      akcii <- r[2]}
    rezult <- suma + akcii*open[i]
    gra <- c(gra, rezult, k, j)}} # ������ ��� ����������� �� rezult � �� ��� ��.�����. �� ��������� 
for (i in 1:length(gra)) { # ����� �� ��������� �� ����������� ��������
  if (gra[i] == max(gra)) {
    nsr <- gra[i+1]
    ksr <- gra[i+2]  
    i <- length(gra)+10 }}
srar_ <- c(nsr, ksr, max(gra))
print(max(gra)); print(nsr); print(ksr)


#-------------------------------------------------------------------------
gra <- c() 
for (k in 2:24) { # 
  for (j in (k+1):25) { 
    suma <- 100000 
    akcii <- 0 
    for (i in 30:ndata) { 
      r <- hod_srar_pr(i, j, k, suma, akcii)
      suma <- r[1]
      akcii <- r[2]}
    rezult <- suma + akcii*open[i]
    gra <- c(gra, rezult, k, j)}} # ������ ��� ����������� �� rezult � �� ��� ��.�����. �� ��������� 
for (i in 1:length(gra)) { # ����� �� ��������� �� ����������� ��������
  if (gra[i] == max(gra)) {
    nsr <- gra[i+1]
    ksr <- gra[i+2]
    i <- length(gra)+10 }}
srar_pr_ <- c(nsr, ksr, max(gra))
print(max(gra)); print(nsr); print(ksr)


#  RSI
#-------------------------------------------------------------------------------
rs <- c()
for (j in 5:25) { #  �� ������ ��������� � ������� �� 5:25
  suma <- 100000 # ������� ����
  akcii <- 0 # ������� ���� �����
  for (i in 30:ndata) { # ������, ���������� �����������
    r <- hod_rsi(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  rs <- c(rs, rezult, j)}
for (i in 1:length(rs)) { 
  if (rs[i] == max(rs)) {
    nj <- rs[i+1]
    i <- length(rs)+10 }}
rsi_ <-c(nj, max(rs))
print(max(rs)); print(nj)

#  CCI
#-------------------------------------------------------------------------------
rs <- c()
for (j in 5:25) { 
  suma <- 100000 
  akcii <- 0 
  for (i in 30:ndata) { 
    r <- hod_cci(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  rs <- c(rs, rezult, j)}
for (i in 1:length(rs)) { 
  if (rs[i] == max(rs)) {
    nj <- rs[i+1]
    i <- length(rs)+10 }}
cci_ <-c(nj, "-", max(rs))
print(max(rs)); print(nj)

# FI - Force Index
#-------------------------------------------------------------------------------
rs <- c()
for (j in 5:25) { #  
  suma <- 100000 
  akcii <- 0 
  for (i in 30:ndata) { 
    r <- hod_fi(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  rs <- c(rs, rezult, j)}
for (i in 1:length(rs)) { 
  if (rs[i] == max(rs)) {
    nj <- rs[i+1]
    i <- length(rs)+10 }}
fi_ <-c(nj, max(rs))
print(max(rs)); print(nj)

#stochastic indicator
#----------------------------------------------------------------------------
rs <- c()
for (j in 5:25) {  
  suma <- 100000 
  akcii <- 0 
  for (i in 50:ndata) { 
    r <- hod_sholast1(i, j, suma, akcii)
    #    r <- hod_sholast2(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  rs <- c(rs, rezult, j)}
for (i in 1:length(rs)) { 
  if (rs[i] == max(rs)) {
    nj <- rs[i+1]
    i <- length(rs)+10 }}
sholast1_ <-c(nj, max(rs))
print(max(rs)); print(nj)

#WPR
#----------------------------------------------------------------------------
rs <- c()
for (j in 5:25) { 5
  suma <- 100000 
  akcii <- 0 
  for (i in 50:ndata) { 
    r <- hod_wpr(i, j, suma, akcii)
    suma <- r[1]
    akcii <- r[2]}
  rezult <- suma + akcii*open[i]
  rs <- c(rs, rezult, j)}
for (i in 1:length(rs)) { 
  if (rs[i] == max(rs)) {
    nj <- rs[i+1]
    i <- length(rs)+10 }}
wpr_ <-c(nj, max(rs))
print(max(rs)); print(nj)


#----------------------------------------------------------------------------
pre <- c(extr_[2], srar_[3], rsi_[2], fi_[2], sholast1_[2], wpr_[2])
pre1 <- sort(pre)
npre <- length(pre)
for (i in 1:npre) {
  if (extr_[2] == pre1[i]) {
    extr_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (srar_[3] == pre1[i]) {
    srar_[3] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (rsi_[2] == pre1[i]) {
    rsi_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (fi_[2] == pre1[i]) {
    fi_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (sholast1_[2] == pre1[i]) {
    sholast1_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (wpr_[2] == pre1[i]) {
    wpr_[2] <- i; i <= npre+10}}

r1 <- 0 # 
r2 <- 0 # 
r3 <- 0 # 

i <- ndata


#----------------------------------------------------------------------------
pre <- c(extr_[2], srar_[3], rsi_[2], fi_[2], sholast1_[2], wpr_[2])
pre1 <- sort(pre)
npre <- length(pre)
for (i in 1:npre) {
  if (extr_[2] == pre1[i]) {
    extr_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (srar_[3] == pre1[i]) {
    srar_[3] <- i; i <= npre+10}}
for (i in 1:npre) {
  if ( rsi_[2] == pre1[i]) {
    rsi_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (fi_[2] == pre1[i]) {
    fi_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (sholast1_[2] == pre1[i]) {
    sholast1_[2] <- i; i <= npre+10}}
for (i in 1:npre) {
  if (wpr_[2] == pre1[i]) {
    wpr_[2] <- i; i <= npre+10}}

r1 <- 0 
r2 <- 0 
r3 <- 0 

i <- ndata

#Output from several indicators accumulated
#------------------------------------------------------------------------
# if (optim_cci(i, cci_[1]) == "Do not enter a position") r1 <- r1+cci_[2]
# if (optim_cci(i, cci_[1]) == "Sell") r2 <- r2+cci_[2]
# if (optim_cci(i, cci_[1]) == "Buy") r3 <- r3+cci_[2]

if (optim_fi(i, fi_[1]) == "Do not enter a position") r1 <- r1+fi_[2]
if (optim_fi(i, fi_[1]) == "Sell") r2 <- r2+fi_[2]
if (optim_fi(i, fi_[1]) == "Buy") r3 <- r3+fi_[2]

if (optim_rsi(i, rsi_[1]) == "Do not enter a position") r1 <- r1+rsi_[2]
if (optim_rsi(i, rsi_[1]) == "Sell") r2 <- r2+rsi_[2]
if (optim_rsi(i, rsi_[1]) == "Buy") r3 <- r3+rsi_[2]

if (optim_extr(i, extr_[1]) == "Do not enter a position") r1 <- r1+extr_[2]
if (optim_extr(i, extr_[1]) == "Sell") r2 <- r2+extr_[2]
if (optim_extr(i, extr_[1]) == "Buy") r3 <- r3+extr_[2]

if (optim_wpr(i, wpr_[1]) == "Do not enter a position") r1 <- r1+wpr_[2]
if (optim_wpr(i, wpr_[1]) == "Sell") r2 <- r2+wpr_[2]
if (optim_wpr(i, wpr_[1]) == "Buy") r3 <- r3+wpr_[2]

# if (optim_alig1(i) == "Do not enter a position") r1 <- r1+alig1_[1]
# if (optim_alig1(i) == "Sell") r2 <- r2+alig1_[1]
# if (optim_alig1(i) == "Buy") r3 <- r3+alig1_[1]

# if (optim_alig2_(i]) == "Do not enter a position") r1 <- r1+alig2_[1]
# if (optim_alig2_(i]) == "Sell") r2 <- r2+alig2_[1]
# if (optim_alig2_(i]) == "Buy") r3 <- r3+alig2_[1]

# if (optim_alig3_(i]) == "Do not enter a position") r1 <- r1+alig3_[1]
# if (optim_alig3_(i]) == "Sell") r2 <- r2+alig3_[1]
# if (optim_alig3_(i]) == "Buy") r3 <- r3+alig3_[1]

if (optim_sholast1(i, sholast1_[1]) == "Do not enter a position") r1 <- r1+sholast1_[2]
if (optim_sholast1(i, sholast1_[1]) == "Sell") r2 <- r2+sholast1_[2]
if (optim_sholast1(i, sholast1_[1]) == "Buy") r3 <- r3+sholast1_[2]

# if (optim_sholast2(i, sholast2_[1]) == "Do not enter a position") r1 <- r1+sholast2_[2]
# if (optim_sholast2(i, sholast2_[1]) == "Sell") r2 <- r2+sholast2_[2]
# if (optim_sholast2(i, sholast2_[1]) == "Buy") r3 <- r3+sholast2_[2]

if (optim_srar(i, srar_[1], srar_[2]) == "Do not enter a position") r1 <- r1+srar_[3]
if (optim_srar(i, srar_[1], srar_[2]) == "Sell") r2 <- r2+srar_[3]
if (optim_srar(i, srar_[1], srar_[2]) == "Buy") r3 <- r3+srar_[3]

# if (optim_srar_pr(i, srar_pr_[1], srar_pr_[2]) == "Do not enter a position") r1 <- r1+srar_pr_[3]
# if (optim_srar_pr(i, srar_pr_[1], srar_pr_[2]) == "Sell") r2 <- r2+srar_pr_[3]
# if (optim_srar_pr(i, srar_pr_[1], srar_pr_[2]) == "Buy") r3 <- r3+srar_pr_[3]

# if (optim_srar_exp(i, srar_exp_[1], srar_exp_[2]) == "Do not enter a position") r1 <- r1+srar_exp_[3]
# if (optim_srar_exp(i, srar_exp_[1], srar_exp_[2]) == "Sell") r2 <- r2+srar_exp_[3]
# if (optim_srar_exp(i, srar_exp_[1], srar_exp_[2]) == "Buy") r3 <- r3+srar_exp_[3]


t <- fi_[2]+rsi_[2]+wpr_[2]+sholast1_[2]+extr_[2]+srar_[3]
r <- r2+r3
otg <- "Do not enter a position"
if (r > 0) otg <- "Buy" 
if (r < 0) otg <- "Sell"
print(otg)                  
print(r/t)             #how likely the success is     


b2 <- c("SMA", "WMA", "EMA", "RSI", "CCI", "FI", "WilliamsPR", "Alligator", "Extremes", "AI")

b1 <- c("SMA", "WMA", "EMA")

l<-formatC(c(srar_, srar_pr_, srar_ex_), format="f", digits=4)



descriptive<-matrix(l,ncol=3,byrow=TRUE)
rownames(descriptive)<-b1
c1<-c("shortterm","longterm","profit") 
colnames(descriptive)<-c1


