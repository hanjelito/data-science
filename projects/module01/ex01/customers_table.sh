# sudo -u postgres psql -c "\dt+ piscineds"
# data=$(sudo -u postgres psql -d piscineds -c "\dt" | grep "data_20")
# echo "${data}"
data=$(sudo -u postgres psql -d piscineds -c "\dt" | grep "data_20" | awk '{print $3}')
echo "${data}"
# sudo -u postgres psql -c "\c piscineds" -c "SELECT * FROM data_2023_feb LIMIT 20;" > test.txt