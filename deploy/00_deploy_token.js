const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

// Run with `genlayer deploy` while the CLI network is set to studionet.
// The CLI supplies its active, unlocked account through `client`.
module.exports = async function deployTokenClaimCapabilityGate(client) {
  const root = path.resolve(__dirname, "..");
  const candidate = fs.readFileSync(
    path.join(root, "docs", "STUDIONET_RELEASE_CANDIDATE.md"),
    "utf8",
  );
  const block = candidate.match(/```json\s*([\s\S]*?)\s*```/);
  if (!block) throw new Error("Missing candidate constructor JSON");

  const args = JSON.parse(block[1]);
  if (!Array.isArray(args) || args.length !== 6 || args.slice(0, 4).some((arg) => typeof arg !== "string")) {
    throw new Error("Candidate constructor must contain six positional arguments");
  }
  const context = JSON.parse(args[2]);
  const urls = JSON.parse(args[3]);
  if (context.chain !== "eip155:1" || urls.length !== 1 || !urls[0].startsWith("https://sourcify.dev/")) {
    throw new Error("Unexpected StudioNet candidate evidence inputs");
  }

  const code = fs.readFileSync(
    path.join(root, "contracts", "token_claim_capability_gate.py"),
    "utf8",
  );
  console.log(`source_sha256=${crypto.createHash("sha256").update(code).digest("hex")}`);
  const hash = await client.deployContract({ code, args, leaderOnly: false });
  console.log(`deployment_transaction=${hash}`);
};
