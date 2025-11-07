export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  rfid_tag: string | null;
  created_at: string;
}

export interface Threshold {
  id: number;
  min_humidity: number;
  max_humidity: number;
  min_temperature: number;
  max_temperature: number;
  created_at: string;
  updated_at: string;
}

export interface Read {
  id: number;
  name: string;
  user_id: number | null;
  timestamp: string;
  created_at: string;
  pump: Pump | null;
  sensor: Sensor | null;
  fan: Fan | null;
}
export interface Pump {
  id: number;
  read_id: number;
  name: string;
  status: boolean;
}

export interface Sensor {
  id: number;
  read_id: number;
  name: string;
  humidity: number;
  temperature: number;
}

export interface Fan {
  id: number;
  read_id: number;
  name: string;
  status: boolean;
}

export interface Access {
  id: number;
  user_id: number;
  timestamp: string;
}
