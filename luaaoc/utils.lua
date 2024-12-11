local M = {}

local BASE_PTH = os.getenv("HOME") .. "/hobby/aoc24/data/"

---Get path to data file for a given day
---@param day integer
---@return string
function M.get_data_path(day)
  return BASE_PTH .. "day" .. day
end

---Read file contents
---@param day integer
---@return string | nil
function M.read_contents_from(day)
  local pth = M.get_data_path(day)

  local file = io.open(pth, "r")
  if not file then
    return nil
  end

  local content = file:read("*a")
  file:close()

  return content
end

---Read lines from file
---@param day integer
---@return string[] | nil
function M.read_lines_from(day)
  local contents = M.read_contents_from(day)

  if not contents then
    return contents
  end

  ---@type string[]
  local lines = {}

  for line in contents:gmatch("[^\r\n]+") do
    if #line == 0 then
      goto continue
    end

    table.insert(lines, line)

    ::continue::
  end

  return lines
end

---Split a string by the separator [default whitespace]
---@param s string
---@param sep? string
---@return string[] parts
function M.str_split(s, sep)
  if sep == nil then
    sep = "%s"
  end

  ---@type string[]
  local parts = {}

  for part in s:gmatch("([^" .. sep .. "]+)") do
    table.insert(parts, part)
  end

  return parts
end

return M
