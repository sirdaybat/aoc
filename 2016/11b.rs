use std::fmt;
use std::collections::{VecDeque, HashSet};
use std::io;

#[derive(Debug)]
#[derive(PartialEq)]
enum Elem{
	/*
	Hydrogen = 0,
	Lithium = 1,
	*/

	Strontium = 0,
	Plutonium = 1,
	Thulium = 2,
	Ruthenium = 3,
	Curium = 4,
	Elerium = 5,
	Dilithium = 6,
	
	Last
}

fn int_to_elem(i: i32) -> Elem {
	match i {
		/*
		0 => Elem::Hydrogen,
		1 => Elem::Lithium,
		*/

		0 => Elem::Strontium,
		1 => Elem::Plutonium,
		2 => Elem::Thulium,
		3 => Elem::Ruthenium,
		4 => Elem::Curium,
		5 => Elem::Elerium,
		6 => Elem::Dilithium,
		
 		_ => { assert!(false); Elem::Last },
	}
}

impl fmt::Display for Elem {
	fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		fmt::Debug::fmt(self, f)
	}
}

fn main(){
	#[derive(Debug)]
	#[derive(Clone, Copy)]
	#[derive(PartialEq, Eq, Hash)]
	struct FloorState{
		gens: u8,
		chips: u8,
	}
	
	const NUM_FLOORS : u8 = 4;

	#[derive(Debug)]
	#[derive(Clone, Copy)]
	#[derive(PartialEq, Eq, Hash)]
	struct State{
		floors: [FloorState; NUM_FLOORS as usize],
		cur_floor: u8,
	}
	
	/*
	let initial_state = State{
		cur_floor: 0,
		floors: [
			FloorState{ gens: 0, chips: 1<<(Elem::Hydrogen as u8) | 1<<(Elem::Lithium as u8) },
			FloorState{ gens: 1<<(Elem::Hydrogen as u8), chips: 0 },
			FloorState{ gens: 1<<(Elem::Lithium as u8), chips: 0 },
			FloorState{ gens: 0, chips: 0 },
		],
	};
	*/
	
	let initial_state = State{
		cur_floor: 0,
		floors: [
			FloorState{ gens: 1<<(Elem::Strontium as u8)|1<<(Elem::Plutonium as u8)|1<<(Elem::Elerium as u8)|1<<(Elem::Dilithium as u8), chips: 1<<(Elem::Strontium as u8)|1<<(Elem::Plutonium as u8)|1<<(Elem::Elerium as u8)|1<<(Elem::Dilithium as u8) },
			FloorState{ gens: 1<<(Elem::Thulium as u8)|1<<(Elem::Ruthenium as u8)|1<<(Elem::Curium as u8), chips: 1<<(Elem::Ruthenium as u8)|1<<(Elem::Curium as u8) },
			FloorState{ gens: 0, chips: 1<<(Elem::Thulium as u8) },
			FloorState{ gens: 0, chips: 0 },
		],
	};
	
	fn print_state(state: &State){
		for floor_idx in (0..NUM_FLOORS).rev() {
			print!("F{} ", floor_idx+1);
			if floor_idx == state.cur_floor {
				print!("E");
			}
			else {
				print!(".");
			}
			print!("  ");
			
			let f = &state.floors[floor_idx as usize];
			
			for i in 0..(Elem::Last as u8) {
				if f.gens & (1<<i) != 0 {
					print!("{}G ", &int_to_elem(i as i32).to_string()[..1]);
				}
				else {
					print!(".  ");
				}
				
				if f.chips & (1<<i) != 0 {
					print!("{}M ", &int_to_elem(i as i32).to_string()[..1]);
				}
				else {
					print!(".  ");
				}
			}
			
			println!("");
		}
		
		println!("");
	}

	fn is_valid_state(state: &State) -> bool {
		for floor in state.floors.iter() {
			if floor.gens != 0 && floor.chips & floor.gens != floor.chips {
				return false;
			}
		}
		return true;
	}

	assert!(is_valid_state(&initial_state));

	fn is_goal(state: &State) -> bool {
		if state.cur_floor != NUM_FLOORS-1 {
			return false;
		}
		for floor_idx in 0..state.floors.len()-1 {
			let floor = &state.floors[floor_idx];
			if floor.gens != 0 || floor.chips != 0 {
				return false;
			}
		}
		return true;
	}

	//let mut visited_states : Vec<State> = Vec::new();
	let mut visited_states : HashSet<State> = HashSet::new();
	//let mut is_visited : [bool; 4194304];
	let mut queue0 : VecDeque<State> = VecDeque::new();
	let mut queue1 : VecDeque<State> = VecDeque::new();
	
	let mut queue = &mut queue0;
	let mut queue_other = &mut queue1;

	visited_states.insert(initial_state);
	//is_visited[state_index(initial_state)] = true;
	queue.push_back(initial_state);
	
	let mut num_tests_done = 0;

	let mut dist = 1;
	'mainloop: while queue.len() > 0 {
		while queue.len() > 0 {
			let state = queue.pop_front().unwrap();
			
			//print_state(&state);
			//io::stdin().read_line(&mut String::new());
		
			for &dir in [-1i32, 1i32].iter() {
				let new_floor_i32 = (state.cur_floor as i32) + dir;
				if new_floor_i32 < 0 || new_floor_i32 >= NUM_FLOORS as i32 {
					continue;
				}
				let new_floor = new_floor_i32 as u8;
				
				let mod_state = |new_state: &mut State, bit: u16| {
					assert!(bit != 0 && bit & (bit-1) == 0);
					let nfs = &mut new_state.floors;
					if bit < (1<<8) {
						assert!(nfs[state.cur_floor as usize].chips & (bit as u8) == bit as u8);
						nfs[state.cur_floor as usize].chips &= !(bit as u8);
						nfs[new_floor as usize].chips |= bit as u8;
					}
					else {
						assert!(nfs[state.cur_floor as usize].gens & ((bit >> 8) as u8) == (bit >> 8) as u8);
						nfs[state.cur_floor as usize].gens &= !((bit >> 8) as u8);
						nfs[new_floor as usize].gens |= (bit >> 8) as u8;
					}
				};
				
				let mut try_add_state = |new_state: State| {
					//if is_valid_state(&new_state) && !visited_states.iter().any(|&s| s == new_state) {
					num_tests_done += 1;
					if is_valid_state(&new_state) && !visited_states.contains(&new_state) {
					//if is_valid_state(&new_state) && !is_visited[state_index(new_state)] {
						//println!("NEW: ");
						//print_state(&new_state);
						assert!(new_state.floors[new_state.cur_floor as usize].gens != 0 || new_state.floors[new_state.cur_floor as usize].chips != 0);
					
						visited_states.insert(new_state);
						queue_other.push_back(new_state);
					}
				};
				
				let f = &state.floors[state.cur_floor as usize];
				let objs = (f.gens as u16) << 8 | (f.chips as u16);
				
				let mut oi0 = objs;
				
				while oi0 > 0 {
					let oi0_lobit = oi0 & (!oi0 + 1);
					oi0 &= !oi0_lobit;
					
					{
						let mut new_state = state;
						new_state.cur_floor = new_floor;
						mod_state(&mut new_state, oi0_lobit);
						try_add_state(new_state);
						
						if is_goal(&new_state) {
							println!("GOAL {}", dist);
							break 'mainloop;
						}
					}

					let mut oi1 = oi0;
					while oi1 > 0 {
						let oi1_lobit = oi1 & (!oi1 + 1);
						oi1 &= !oi1_lobit;
						
						let mut new_state = state;
						new_state.cur_floor = new_floor;
						mod_state(&mut new_state, oi0_lobit);
						mod_state(&mut new_state, oi1_lobit);

						try_add_state(new_state);
						
						if is_goal(&new_state) {
							println!("GOAL {}", dist);
							break 'mainloop;
						}
					}
				}
			}
		}
		
		std::mem::swap(queue, queue_other);
		
		dist += 1;

		println!("foo {}; {} {} {}", dist, visited_states.len(), queue.len(), num_tests_done);
	}
}
