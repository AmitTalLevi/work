# Run docker-compose:
    - docker-compose up -d
# Check if docker running:
    - docker ps
    OR
    -docker ps -a 
# Check that you could connect:
    - docker exec -it my-mysql mysql -u root -p
    OR if you want show DB
    - docker-compose exec mysql mysql -u root -p -e "SHOW DATABASES;"
# Remove proccess
    - docker rm -f XXXXX