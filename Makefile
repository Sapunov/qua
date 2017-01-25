	.PHONY: build install dist srpm rpm pypi clean

	PYTHON		?=python3.5
	NAME		?=qua
	USER		?=qua


	install:
		mkdir -p /var/log/$(NAME) /var/lib/$(NAME) /etc/$(NAME)
		mkdir -p /var/lib/$(NAME)/data/cache
		mkdir -p /var/lib/$(NAME)/data/search_index
		mkdir -p /var/lib/$(NAME)/data/static

		chown -R $(USER):$(USER) /var/log/$(NAME)

		cp -R qua/* /var/lib/$(NAME)/

		chown -R $(USER):$(USER) /var/lib/$(NAME)

		chmod +x admin/*

	dist:
		rm -rf dist
		tar -czvf $(NAME).tgz qua admin manage.py Makefile
		mkdir dist && mv $(NAME).tgz dist
