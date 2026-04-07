# Optional local build (same command as CMake target output layout when BUILDDIR=book).
# Prefer: cmake --build build -- docs  (writes ../build/docs/book from your build tree)
.PHONY: html clean
html:
	sphinx-build -b html . book
clean:
	rm -rf book .doctrees
