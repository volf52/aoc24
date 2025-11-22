const std = @import("std");

const utils = @import("utils.zig");

fn read_data() !void {}

pub fn main() !void {
    std.debug.print("Hello\n", .{});

    const pth = utils.get_data_file_path(1);

    std.debug.print("path is {}", .{
        pth,
    });
}
