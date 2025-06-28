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

        -- Commande spéciale : sauvegarde
    if cmd == "SAVE" then
      local save_path = "C:/Users/moran/Desktop/VJMon/"
      local filename = save_path .. "Save_" .. os.date("%d-%m-%Y_%H-%M-%S") .. ".State"

      savestate.save(1, filename)

      print("💾 Sauvegarde manuelle :", filename)

      local file = io.open(filename, "r")
      if file then
        file:close()
        print("📁 Fichier sauvegarde trouvé !")
      else
        print("❌ Le fichier n’a pas été écrit sur le disque.")
      end
    end


    -- On ne lance le maintien que si la commande est une touche valide
    local valid_keys = {up=true, down=true, left=true, right=true, A=true, B=true, X=true, Y=true}
    if valid_keys[cmd] then
      frames_to_press = 10
      current_key = cmd
      print("Début pression touche", current_key, "pour 18 frames")
    else
      if cmd ~= "SAVE" then
        print("Commande inconnue :", cmd)
      end
    end
  end

  local pad = {
    up = false, down = false, left = false, right = false,
    a = false, b = false, start = false, select = false,
    r = false, l = false, x = false, y = false,
    debug = false, lid = false
  }

  if frames_to_press > 0 and current_key then
    pad[current_key] = true
    frames_to_press = frames_to_press - 1
    print("Touche", current_key, "maintenue, frames restantes :", frames_to_press)
  end

  joypad.set(pad)
end

emu.registerafter(onFrame)
