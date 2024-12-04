use std::{
    env::current_dir,
    fs::{self, canonicalize},
    path::PathBuf,
};

pub fn get_data_path(day: u8) -> PathBuf {
    let exe_pth = current_dir().expect("current dir not extracted");
    let df_pth = exe_pth.join(format!("../data/day{day}"));
    let abs_df_pth = canonicalize(df_pth).expect("cannot canonicalize the path");

    if !abs_df_pth.exists() {
        panic!("{:?} does not exist", abs_df_pth);
    }

    abs_df_pth
}

pub fn read_day_file(day: u8) -> String {
    let pth = get_data_path(day);

    fs::read_to_string(pth).unwrap()
}

pub fn read_day_lines(day: u8) -> Vec<String> {
    let contents = read_day_file(day);

    contents.lines().map(str::to_string).collect::<Vec<_>>()
}
