#!/usr/bin/env python3
"""Smoke test for receipt-ocr package."""

import sys


def main():
    """Test that the package can be imported and basic functionality works."""
    try:
        import receipt_ocr  # noqa: F401
        from receipt_ocr.__about__ import __version__

        print(f"✓ receipt-ocr {__version__} imported successfully")

        # Test that main modules can be imported
        from receipt_ocr import cli, parsers, processors, providers, utils  # noqa: F401

        print("✓ All core modules importable")

        return 0
    except Exception as e:
        print(f"✗ Smoke test failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
