-- AI Chat HUD addon for helper.xpl
-- Adds persistent chat overlay to the game HUD

local ai_hud = {
    name = "AIChatHUD",
    frame = nil,
    table = nil,
    messages = {},
    max_messages = 8,
    last_update = 0,
}

-- Register for Helper's onUpdate callback
if Helper and Helper.uix_callbacks then
    if not Helper.uix_callbacks["onUpdate"] then
        Helper.uix_callbacks["onUpdate"] = {}
    end
    Helper.uix_callbacks["onUpdate"]["ai_chat_hud"] = function()
        ai_hud.update()
    end
end

-- Register as menu so it's tracked
Menus = Menus or {}
table.insert(Menus, ai_hud)

function ai_hud.update()
    local now = getElapsedTime()
    if now - ai_hud.last_update < 0.5 then
        return
    end
    ai_hud.last_update = now
    
    -- Create frame if needed
    if not ai_hud.frame then
        ai_hud.create_frame()
    end
    
    -- Update content
    if ai_hud.frame then
        ai_hud.refresh()
    end
end

function ai_hud.create_frame()
    -- Try to find an existing frame to attach to
    -- For now, just log that we're ready
    DebugError("[AI Chat HUD] Frame creation requested")
end

function ai_hud.refresh()
    -- Update HUD content
end

function ai_hud.add_message(text, is_ai)
    table.insert(ai_hud.messages, {
        text = text,
        is_ai = is_ai,
    })
    while #ai_hud.messages > ai_hud.max_messages do
        table.remove(ai_hud.messages, 1)
    end
end

DebugError("[AI Chat HUD] Addon loaded")
