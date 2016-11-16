-- Filename: DB_004副本 4.lua
-- Author: auto-created by kong`s ParseExcel(to lua) tool.
-- methods: X.keys = {}, X.getDataById(id), X.getArrDataByField(fieldName, fieldValue)
-- Function: no description.

local keys = {
	"key1","key2","key3","key4","key5","key6","key7","key8","key9","key10"
}

local data = {
	id1={1, 78.1, 5, 3, 2, 5, nil, 6, 6, "6.0", 6},
	id2={2, 4, 5, 3, 2, 105, 3, 106, 2, "2.0", -1},
	id3={3, -1, 4, 5, 3, 2, 5, 3, 6, "2.0", -1},
	id4={4, -1, 4, 5, 3, 2, 5, 3, 6, "-1.0", -1},
	id5={5, -1, -1, 4, 5, 3, 2, 5, 3, "6.0", -1},
	id6={6, -1, -1, 4, 5, 3, 2, 5, 3, "6.0", -1},
	id7={7, 4, 4, 4, 4, 5, 3, 2, 5, "3.0", 6},
	id8={8, 5, 5, 5, 3, 2, 5, 3, 2, "2.0", 2},
	id9={9, -1, -1, 5, 3, 2, 5, 3, 2, "-1.0", -1},
	id10={10, -1, 5, 3, 2, 5, 3, 2, -1, "-1.0", -1},
	id11={11, -1, 5, 3, 2, 5, 3, 2, -1, "-1.0", -1},
	id12={12, 5, 3, 2, 5, 3, 2, -1, -1, "-1.0", -1},
}

DB_004副本 4 = DB_Template.new (keys, data)
return DB_004副本 4