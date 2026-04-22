-- ai_telemetry.xpl
-- Reads player ship position, speed and rotation every 0.5s
-- Stores data in global AITelemetry table accessible from MD via GetNPCBlackboard

AITelemetry = AITelemetry or {
    position   = { x = 0, y = 0, z = 0 },
    speed      = 0,
    maxSpeed   = 0,
    rotation   = { yaw = 0, pitch = 0, roll = 0 },
    sectorName = "",
    shipName   = "",
    shipClass  = "",
    lastUpdate = 0,
}

local UPDATE_INTERVAL = 0.5

local function updateTelemetry()
    local now = getElapsedTime()
    if now - AITelemetry.lastUpdate < UPDATE_INTERVAL then return end
    AITelemetry.lastUpdate = now

    -- Get player ship
    local playership = ConvertStringTo64Bit(tostring(C.GetPlayerObjectID()))
    if not playership or playership == 0 then return end

    -- Position
    local pos = C.GetObjectPositionInSector(playership)
    if pos then
        AITelemetry.position.x = math.floor(pos.x)
        AITelemetry.position.y = math.floor(pos.y)
        AITelemetry.position.z = math.floor(pos.z)
    end

    -- Speed
    local speed = C.GetObjectSpeed(playership)
    if speed then
        AITelemetry.speed = math.floor(speed * 10) / 10
    end

    -- Max speed (from ship stats)
    local stats = C.GetShipPilotBuildSpeed(playership)
    if stats then
        AITelemetry.maxSpeed = math.floor(stats.max * 10) / 10
    end

    -- Rotation
    local rot = C.GetObjectRotation(playership)
    if rot then
        AITelemetry.rotation.yaw   = math.floor(math.deg(rot.yaw)   * 10) / 10
        AITelemetry.rotation.pitch = math.floor(math.deg(rot.pitch) * 10) / 10
        AITelemetry.rotation.roll  = math.floor(math.deg(rot.roll)  * 10) / 10
    end

    -- Sector name
    local sector = GetPlayerCurrentSector and GetPlayerCurrentSector()
    if sector then
        AITelemetry.sectorName = GetComponentData(sector, "name") or ""
    end

    -- Ship name and class
    AITelemetry.shipName  = GetComponentData(playership, "name")  or ""
    AITelemetry.shipClass = GetComponentData(playership, "class") or ""
end

-- Hook into Helper update loop
if Helper and Helper.uix_callbacks then
    if not Helper.uix_callbacks["onUpdate"] then
        Helper.uix_callbacks["onUpdate"] = {}
    end
    Helper.uix_callbacks["onUpdate"]["ai_telemetry"] = function()
        updateTelemetry()
    end
end

DebugError("[AI Telemetry] Loaded")
