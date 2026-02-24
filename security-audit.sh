export DOCKER_CONTAINER_ID=$(docker ps -q --filter "ancestor=dev-0x0001/workspace" | head -n 1)

docker exec -it ${DOCKER_CONTAINER_ID} sh -c \
"source ~/.profile && echo \"Exported from container:\" && env | grep -E 'USER|PATH|HOME'"

docker exec -it ${DOCKER_CONTAINER_ID} sh -c \
"echo \"UID Mapping:\" && id -u && id -g && groups"

docker exec -it ${DOCKER_CONTAINER_ID} sh -c \
"echo \"Mount Points:\" && mount | grep '/dev/'