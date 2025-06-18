local frames_to_press = 0
local current_key = nil

local function onFrame()
  local file = io.open("input.txt", "r")
  local cmd = nil
  if file then
    cmd = file:read("*l")
    file:close()
    io.open("input.txt", "w"):close()
  end

  if cmd then
    print("Commande reçue :", cmd)
    -- On met en minuscules pour gérer sans casse
  

    -- On ne lance le maintien que si la commande est une touche valide
    local valid_keys = {up=true, down=true, left=true, right=true, A=true, B=true}
    if valid_keys[cmd] then
      frames_to_press = 10
      current_key = cmd
      print("Début pression touche", current_key, "pour 10 frames")
    else
      print("Commande inconnue:", cmd)
    end
  end

  local pad = {
    up = false,
    down = false,
    left = false,
    right = false,
    a = false,
    b = false,
    start = false,
    select = false,
    r = false,
    l = false,
    x = false,
    y = false,
    debug = false,
    lid = false
  }

  if frames_to_press > 0 and current_key then
    pad[current_key] = true
    frames_to_press = frames_to_press - 1
    print("Touche", current_key, "maintenue, frames restantes :", frames_to_press)
  end

  joypad.set(pad)
end

emu.registerafter(onFrame)
