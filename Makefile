git_short_hash = `git rev-parse --short HEAD`
project_name = 'token-issuer'
image := $(shell docker images -q ${project_name}:${git_short_hash})
tag = '0.6.0'

create-image-tagged:
	echo "creating image"
	echo "docker build ${project_name}:$(tag)"
	docker build -t $(project_name):$(tag) .

create-image:
	echo "creating image"
	echo "docker build ${project_name}:$(git_short_hash)"
	docker build -t $(project_name):$(git_short_hash) . --no-cache

push-image: create-image
	echo "pushing image"
	docker push $(project_name):$(git_short_hash)

run-image: create-image
	echo "running image"
	docker run --name $(project_name) -e TOKEN_ISSUER_SECRET=YOUR_SECRET -e TOKEN_ISSUER_IDENTIFIER=YOUR_IDENTIFIER -d $(project_name):$(git_short_hash)

run-image-locally: create-image-tagged
	echo "running image"
	docker run --name $(project_name) -e TOKEN_ISSUER_SECRET=YOUR_SECRET -e TOKEN_ISSUER_IDENTIFIER=YOUR_IDENTIFIER -d -p 5000:5000 $(project_name):$(tag)
