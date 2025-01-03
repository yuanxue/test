
import ast
import base64
import json
import re

from typing import Any
import raw_data



def python_function_def_to_json(func_str: str) -> dict[str, Any]:
  """Converts a Python function definition string to a JSON format.

  Args:
    func_str: The string containing the Python function definition.

  Returns:
    A JSON string representing the function.
  """
  try:
    # Parse the function string into an AST tree
    tree = ast.parse(func_str)

    # Find the function definition node
    function_def = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))

    # Extract function name and docstring
    name = function_def.name
    docstring = ast.get_docstring(function_def) or ""

    # Extract parameters and their types
    parameters = {
        "type": "any",
        "required": [],
        "properties": {}
    }
    for arg in function_def.args.args:
      param_name = arg.arg
      param_type = "any"  # Default type if no annotation
      if arg.annotation:
        if isinstance(arg.annotation, ast.Name):
          param_type = arg.annotation.id
        elif isinstance(arg.annotation, ast.Subscript):
          param_type = f"{arg.annotation.value.id}[{arg.annotation.slice.value.id}]"  # For types like list[str]

      param_info = {
          "type": param_type,
          "description": "",  # Add description if available
      }
      # Currently, default values and kind (keyword-only) are not extracted from the string
      # You'll need more advanced AST parsing to get those details

      parameters["properties"][param_name] = param_info

    json_data = {
        "name": name,
        "description": docstring,
        "parameters": parameters
    }

    return json_data

  except Exception as e:
    print(f"Error parsing function string: {e}")
    return None
  
def _parse_function_name(function_invocation) -> str| None:
    # Regular expression to match the function name
    match = re.match(r'\s*([a-zA-Z_]\w*)\s*\(', function_invocation)
    if match:
        return match.group(1)  # Return the function name
    return None  # Return None if no match is found  

def _parse_arg(expr: ast.Expr) -> Any:
  """Parse ast expr into function call arguments."""
  if isinstance(expr, ast.Constant):
    return expr.value
  elif isinstance(expr, ast.Name):
    return expr.id
  elif isinstance(expr, ast.List):
    return [_parse_arg(x) for x in expr.elts]
  elif isinstance(expr, ast.Dict):
    return {
        _parse_arg(k): _parse_arg(v)
        for k, v in zip(expr.keys, expr.values)
    }
  elif isinstance(expr, ast.UnaryOp):
    if isinstance(expr.op, ast.USub):
      val = _parse_arg(expr.operand)
      val: float | int
      return -val
    else:
      raise ValueError(f"Unsupported operation: {ast.dump(expr.op, indent=4)}")
  elif isinstance(expr, ast.Call):
    return {kw.arg: _parse_arg(kw.value) for kw in expr.keywords}


def _convert_python_func_call_to_json(func_call: str) -> dict[str, Any]:
  function_call
  try:
    parse_tree = ast.parse(func_call)
  except Exception as e:
    print("Function call text: ", func_call, "Exception: ", e, "\n")
    raise SyntaxError(e) from e  

  if len(parse_tree.body) != 1:
    print(
        f"Python function call {func_call} should be parsed into a single object"
    )
    raise SyntaxError(
        "Python function call should be parsed into a single object"
    )
  try:
    call_node = parse_tree.body[0].value
    function_call = {
      'name': call_node.func.id,
      'args': {
        arg.arg: _parse_arg(arg.value) for arg in call_node.keywords
      }
    }

  except Exception as e:
    print("Function text: ", func_call, "Exception: ", e, "\n")
    raise SyntaxError(e) from e
  return function_call


def gen_simple_example(id, image_name, query, ground_truth) -> tuple[dict, dict]:
  ground_truth_func_name = _parse_function_name(ground_truth)
  if ground_truth_func_name not in raw_data.name_to_fun:
    raise ValueError(f'invalid ground truth function name {ground_truth_func_name}')
  func_desc = raw_data.name_to_func[ground_truth_func_name]
  image_path = f'images/{image_name}.png'
  with open(image_path, 'rb') as image_file:
    # Read the file's binary content
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    ex = {
      'id': id,
      'tools': [
        {'function_declarations': [func_desc]}
      ],
      'contents': [
        {
          'role': 'user',
          'parts': [
            {'text': query},
            {'inlineData': {'mimeType': 'image/png',
                            'data': encoded_image}}
          ]
        }
      ],
    }
    ground_truth = {
      'tool_calls': [_convert_python_func_call_to_json(ground_truth)]
    }
  return ex, ground_truth

# Main function
def main():
  print("Available functions:")
  for name, definition in raw_data.name_to_func.items():
    json_definition = python_function_def_to_json(definition)
    print(f"- {name}")
    print(json_definition)

  output_file = "output.jsonl"
  with open(output_file, "w") as file:
    for index, raw_ex in enumerate(raw_data.raw_examples):
      id = f'simple-{index}'
      input_prompt, ground_truth = gen_simple_example(id, raw_ex['image'], raw_ex['query'], raw_ex[''])
      print(input_prompt)
      print(ground_truth)
      input_prompt_str = json.dumps(input_prompt)
      ground_truth_str = json.dumps(ground_truth)
      file.write(input_prompt_str + '\n')

# Run the program
if __name__ == "__main__":
    main()