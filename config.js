const { Client } = require("pg");
const client = new Client("postgresql://theDucks:vJD1ufdJRASpMJypuopW7Q@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dkenthackenough-2373");

function insertScan(roomID, personID) {
  stmt = `insert into Scan(scan_id = (
    select max(scan_id) from Scan) + 1, 
    time = NOW(),
    room_id = (select room_id from Room where room_id = ` + roomID + `),
    person_id = (select person_id from Person where person_id = ` + personID + `));`;

  return executeStmt(stmt);
}

function getPermission(personID) {
  stmt = "select s.person_id, p.* from Person s, Permission p where s.perm_id = p.perm_id and s.person_id = " + personID + ";";s

  return executeStmt(stmt);
}

let stmt = "select * from room;";
//results = executeStmt(stmt);






const executeStmt = async (stmt) => {
  await client.connect();

  try {
    const results = await client.query(stmt);
    //console.log(results);
    return results ;
  } catch (err) {
    console.error("error executing query:", err);
  } finally {
    client.end();
  }
};

await executeStmt(stmt)

