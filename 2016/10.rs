extern crate regex;
use regex::Regex;
use std::fs;
use std::io;
use std::io::BufRead;
use std::env;
use std::collections::HashMap;

macro_rules! get(
        ($ex:expr, $err:expr) => (match $ex {
                Some(e) => e,
                None => { println!("{}", $err); return; }
        })
);

macro_rules! get_res(
        ($ex:expr, $err:expr) => (match $ex {
                Ok(v) => v,
                Err(e) => { println!("{}: {}", $err, e); return; }
        })
);

fn main(){
	let file = get_res!(fs::File::open(get!(env::args().nth(1), "need args")), "can't open file");
	
	let re_bot_init = Regex::new(r"^value (\d+) goes to bot (\d+)$").unwrap();
	let re_bot_give = Regex::new(r"^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$").unwrap();
	
	macro_rules! parse_int(
			($ex:expr) => (get_res!($ex.parse::<i32>(), "syntax error"))
	);
	
	#[derive(Debug)]
	struct Init{
		bot: i32,
		value: i32,
	}
	
	#[derive(Debug)]
	enum Receiver{
		Bot(i32),
		Output(i32),
	}
	
	#[derive(Debug)]
	struct Give{
		giver: i32,
		rec_lo: Receiver,
		rec_hi: Receiver,
	}
	
	let mut inits : Vec<Init> = Vec::new();
	let mut gives : Vec<Give> = Vec::new();
	
	for line_maybe in io::BufReader::new(&file).lines() {
		let line = &get_res!(line_maybe, "can't get line");
		
		if let Some(cap) = re_bot_init.captures(line) {
			inits.push(Init{
				value: parse_int!(cap[1]),
				bot: parse_int!(cap[2]),
			});
		}
		else if let Some(cap) = re_bot_give.captures(line) {
			let rec_type_lo = &cap[2];
			let rec_idx_lo = parse_int!(cap[3]);
			let rec_type_hi = &cap[4];
			let rec_idx_hi = parse_int!(cap[5]);
			
			fn receiver(typ: &str, idx: i32) -> Receiver {
				if typ == "bot" {
					Receiver::Bot(idx)
				}
				else {
					assert!(typ == "output");
					Receiver::Output(idx)
				}
			}
			
			gives.push(Give{
				giver: parse_int!(cap[1]),
				rec_lo: receiver(rec_type_lo, rec_idx_lo),
				rec_hi: receiver(rec_type_hi, rec_idx_hi),
			});
		}
		else{
			assert!(line == "")
		}
	}
	
	#[derive(Debug)]
	struct BotState{
		values: Vec<i32>,
	}
	
	#[derive(Debug)]
	struct OutputState{
		values: Vec<i32>,
	}
	
	let mut bots : HashMap<i32, BotState> = HashMap::new();
	
	for init in inits {
		if !bots.contains_key(&init.bot) {
			bots.insert(init.bot, BotState{ values: Vec::new() });
		}
		bots.get_mut(&init.bot).unwrap().values.push(init.value);
	}
	
	for give in &gives {
		if !bots.contains_key(&give.giver) {
			bots.insert(give.giver, BotState{ values: Vec::new() });
		}
	}
	
	let mut outputs : HashMap<i32, OutputState> = HashMap::new();
	
	loop {
		let mut cur_bot_maybe : Option<i32> = None;
		
		for (bot, state) in &bots {
			if state.values.len() == 2 {
				cur_bot_maybe = Some(*bot);
				break;
			}
		}
		
		if let Some(cur_bot) = cur_bot_maybe {
			let lo;
			let hi;
		
			{
				let cur_bot_state = bots.get_mut(&cur_bot).unwrap();
				lo = *cur_bot_state.values.iter().min().unwrap();
				hi = *cur_bot_state.values.iter().max().unwrap();
				cur_bot_state.values.clear();
			}
			
			if lo == 17 && hi == 61 {
				println!("{} compared {} and {}", cur_bot, lo, hi);
			}
			
			let cur_give = gives.iter().find(|&g| g.giver == cur_bot).unwrap();
			
			let mut give = |value: i32, rec: &Receiver| {
				if let Receiver::Bot(rec_bot) = *rec {
					//println!("{} gives {} to bot {}", cur_bot, value, rec_bot);
					bots.get_mut(&rec_bot).unwrap().values.push(value)
				}
				else if let Receiver::Output(rec_output) = *rec {
					//println!("{} gives {} to output {}", cur_bot, value, rec_output);
					if !outputs.contains_key(&rec_output) {
						outputs.insert(rec_output, OutputState{ values: Vec::new() });
					}
					outputs.get_mut(&rec_output).unwrap().values.push(value);
				}
			};
			
			give(lo, &cur_give.rec_lo);
			give(hi, &cur_give.rec_hi);
		}
		else {
			break;
		}
	}
	
	for (output, &OutputState{ref values}) in &outputs {
		println!("foo {:?} {:?}", output, &values);
	}
	
	let mut r = 1;
	for i in 0..3 {
		for v in &outputs[&i].values {
			r *= *v;
		}
	}
	
	println!("bar {}", r);
}
