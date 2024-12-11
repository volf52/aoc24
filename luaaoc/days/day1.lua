local seq = require("pl.seq")
local utils = require("utils")

local M = {}

---@class Nums
---@field first integer[]
---@field second integer[]

---@return Nums
local read_nums = function()
  local nums = { first = {}, second = {} }

  local lines = utils.read_lines_from(1) or {}
  for _, line in ipairs(lines) do
    local parts = utils.str_split(line)

    if #parts ~= 2 then
      goto continue
    end

    table.insert(nums.first, tonumber(parts[1]))
    table.insert(nums.second, tonumber(parts[2]))

    ::continue::
  end

  table.sort(nums.first)
  table.sort(nums.second)

  return nums
end

function M.part1()
  local nums = read_nums()

  local sum = 0
  for a, b in seq.zip(nums.first, nums.second) do
    sum = sum + math.abs(a - b)
  end

  print("Day 1 part 1: " .. sum)
end

return M
