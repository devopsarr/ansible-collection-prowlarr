default: sanity

TEST_MODULE ?= "prowlarr_indexer"

# Run sanity test
.PHONY: sanity
sanity:
	ansible-test sanity --exclude .github/

# Run integration test
.PHONY: integration
integration:
	ansible-test integration ${TEST_MODULE} -vvv --venv

# Generate doc
.PHONY: doc
doc:
	antsibull-docs sphinx-init --use-current --dest-dir dest devopsarr.prowlarr
	cd dest && ./build.sh
