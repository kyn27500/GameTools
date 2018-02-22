-- Filename: DB_Template_new.lua
-- Author: kong.
-- Function: a template for LUA DB.

local DB_Template = {}

local hcopy = nil

hcopy = function(t_data, t_dest)
    if (type(t_dest) ~= "table") then
        print ("Error, t_dest table must be table type.")
        return nil
    end
    local mt = getmetatable(t_data)
    if mt then
        setmetatable(t_dest, mt)
    end
    for k, v in pairs(t_data) do
        if (type(v) == "table") then
            t_dest[k] = {}
            hcopy(v, t_dest[k]) 
        else
            t_dest[k] = v
        end
    end
    return t_dest
end

DB_Template.new = function(keys, data )
	local obj = {}

	local mt = {}
	mt.__index = function (tbl, key)
		for i = 1, #keys do
			if (keys[i] == key) then
				return tbl[i]
			end
		end
	end

	obj.keys = keys

	obj.getDataById = function (key_id)
		local id_data = data["id"..key_id]
		if id_data == nil then
			return nil
		end
		if getmetatable(id_data) ~= nil then
			return id_data
		end
		setmetatable(id_data, mt)

		return id_data
	end

	obj.getArrDataByField = function (fieldName, fieldValue)
		local arrData = {}
		local fieldNo = 1
		for i=1, #keys do
			if keys[i] == fieldName then
				fieldNo = i
				break
			end
		end
		for k, v in pairs(data) do
			if v[fieldNo] == fieldValue then
				setmetatable (v, mt)
				arrData[#arrData+1] = v
			end
		end

		return arrData
	end

    obj.getArrDataBySeveralFields = function (fieldNames, fieldValues)
        if #fieldNames ~= #fieldValues then return end
        
        local arrData = {}
        local fieldNo = {}
        
        for j=1,#fieldNames do
            for i=1, #keys do
                if keys[i] == fieldNames[j] then 
                    fieldNo[#fieldNo + 1] = i
                    break
                end
            end
        end
        
        for k, v in pairs(data) do
            local count = 0
            for i=1,#fieldNo do
                if v[fieldNo[i]] == fieldValues[i] then
                    count = count + 1
                    if count == #fieldValues then
                        setmetatable (v, mt)
                        arrData[#arrData+1] = v
                    end
                end
            end
        end

        table.sort(arrData , function(a,b)
            if a.id < b.id then return true end
        end)
        
        return arrData
    end
    
	obj.getAllData = function ( ... )
		local allData = {}
		allData = hcopy(data,allData)

		for k, v in pairs(allData) do
			setmetatable (v, mt)
		end

		return allData
	end

	obj.getCount = function ( ... )
		local count = 0
        for k,v in pairs(data) do
			count = count + 1
		end
		return count
	end

	return obj
end

return DB_Template
