-- AI Chat addon for TopLevelMenu
-- Patches menu.createInfoFrame to add AI chat section

local addon = {}

-- Wait for menu to exist, then patch
local function patch()
    if not menu or not menu.createInfoFrame then
        Helper.addDelayedOneTimeCallbackOnUpdate(patch, true, getElapsedTime() + 0.5)
        return
    end
    
    -- Store original
    local orig_createInfoFrame = menu.createInfoFrame
    
    -- Override
    menu.createInfoFrame = function()
        -- Call original first
        orig_createInfoFrame()
        
        -- Now add our section
        if menu.infoFrame then
            local currentH = menu.infoFrame.properties.height or 300
            
            local ftable = menu.infoFrame:addTable(1, {
                width = menu.width,
                x = Helper.borderSize,
                y = currentH + Helper.borderSize,
            })
            
            -- Title
            local tRow = ftable:addRow(true, { fixed = true })
            tRow[1]:createText("AI Assistant", {
                color = Color.text_highlight,
                halign = "center",
                fontsize = Helper.scaleFont(Helper.standardFont, 14),
            })
            
            -- Instructions
            local iRow = ftable:addRow(true, { fixed = true })
            iRow[1]:createText("Type /ai in chat to send messages", {
                color = Color.text_standard,
                halign = "center",
                fontsize = Helper.scaleFont(Helper.standardFont, 10),
            })
            
            -- Update frame height
            menu.infoFrame.properties.height = currentH + 60
        end
    end
    
    DebugError("[AI Chat] TopLevelMenu patched successfully")
end

-- Start patching
patch()
