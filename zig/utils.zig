const std = @import("std");
const fs = std.fs;

pub fn get_data_file_path(day: i16) ![]const u8 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const allocator = gpa.allocator();

    // const cwd = fs.cwd();
    const fpth = try std.fmt.allocPrint(allocator, "day{d}", .{day});
    defer allocator.free(fpth);

    const dataFilePath = try fs.path.join(allocator, .{ "data", fpth });
    return dataFilePath;
}
