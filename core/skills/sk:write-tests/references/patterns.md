# Test Framework Templates

Use these templates when the project has **no existing test files** to learn from. Adapt to the project's specific needs.

---

## Vitest + React Testing Library

```tsx
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ComponentName } from './ComponentName'

describe('ComponentName', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders with default props', () => {
    render(<ComponentName />)
    expect(screen.getByText('expected text')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const onAction = vi.fn()
    render(<ComponentName onAction={onAction} />)
    fireEvent.click(screen.getByRole('button', { name: /submit/i }))
    expect(onAction).toHaveBeenCalledOnce()
  })

  it('displays error state', () => {
    render(<ComponentName error="Something went wrong" />)
    expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong')
  })
})
```

---

## Jest (Node.js)

```ts
import { functionName } from './module'

describe('functionName', () => {
  it('returns expected result for valid input', () => {
    expect(functionName('input')).toBe('expected')
  })

  it('throws on invalid input', () => {
    expect(() => functionName(null)).toThrow('Expected error message')
  })

  it('handles edge case', () => {
    expect(functionName('')).toBe('default')
  })
})

// Mocking example
jest.mock('./dependency', () => ({
  depFunction: jest.fn().mockResolvedValue('mocked'),
}))
```

---

## pytest (Python)

```python
import pytest
from module import function_name


class TestFunctionName:
    def test_returns_expected_for_valid_input(self):
        result = function_name("input")
        assert result == "expected"

    def test_raises_on_invalid_input(self):
        with pytest.raises(ValueError, match="expected message"):
            function_name(None)

    def test_handles_empty_input(self):
        assert function_name("") == "default"


# Fixture example
@pytest.fixture
def sample_data():
    return {"key": "value"}


def test_with_fixture(sample_data):
    result = function_name(sample_data)
    assert result is not None


# Mocking example
def test_with_mock(mocker):
    mock_dep = mocker.patch("module.dependency.dep_function")
    mock_dep.return_value = "mocked"
    result = function_name("input")
    assert result == "mocked"
```

---

## Go testing

```go
package mypackage

import (
	"testing"
)

func TestFunctionName(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
		wantErr  bool
	}{
		{
			name:     "valid input",
			input:    "hello",
			expected: "HELLO",
		},
		{
			name:    "empty input returns error",
			input:   "",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := FunctionName(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("FunctionName() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.expected {
				t.Errorf("FunctionName() = %v, want %v", got, tt.expected)
			}
		})
	}
}
```

---

## Rust

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_input() {
        let result = function_name("input");
        assert_eq!(result, "expected");
    }

    #[test]
    #[should_panic(expected = "error message")]
    fn test_invalid_input_panics() {
        function_name("");
    }

    #[test]
    fn test_returns_none_for_missing() {
        assert!(function_name("missing").is_none());
    }
}
```

---

## Mocha + Chai

```ts
import { expect } from 'chai'
import sinon from 'sinon'
import { functionName } from './module'

describe('functionName', () => {
  afterEach(() => {
    sinon.restore()
  })

  it('should return expected result for valid input', () => {
    const result = functionName('input')
    expect(result).to.equal('expected')
  })

  it('should throw on invalid input', () => {
    expect(() => functionName(null)).to.throw('Expected error message')
  })

  it('should call dependency correctly', () => {
    const stub = sinon.stub(dependency, 'method').returns('mocked')
    const result = functionName('input')
    expect(stub.calledOnce).to.be.true
    expect(result).to.equal('mocked')
  })
})
```
