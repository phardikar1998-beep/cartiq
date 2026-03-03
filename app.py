import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CartIQ",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit chrome
st.markdown("""
<style>
    #MainMenu, header, footer, .stDeployButton { display: none !important; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

JSX_CODE = """import { useState, useEffect, useRef } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";

const STORAGE_KEY = "grocery_tracker_orders";
const BUDGET_KEY = "grocery_tracker_budget";
const INSIGHTS_KEY = "grocery_insights";
const DEFAULT_BUDGET = 500;

const C = {
  lime:"#C8F135", coral:"#FF6B6B", sky:"#4ECDC4", purple:"#A855F7",
  orange:"#FF9F1C", pink:"#FF6EB4", bg:"#0F0F1A", card:"#1A1A2E",
  cardHover:"#1F1F38", text:"#F0F0FF", muted:"#8888AA", border:"#2A2A45",
};

const DONUT_COLORS = {
  Protein:"#FF6B6B", Produce:"#C8F135", Dairy:"#4ECDC4", Pantry:"#FF9F1C",
  Snacks:"#FF6EB4", Beverages:"#A855F7", Frozen:"#60A5FA", Other:"#888888",
};

const TAG = {
  Protein:  {bg:"#FF6B6B22",border:"#FF6B6B",text:"#FF6B6B"},
  Produce:  {bg:"#C8F13522",border:"#C8F135",text:"#C8F135"},
  Dairy:    {bg:"#4ECDC422",border:"#4ECDC4",text:"#4ECDC4"},
  Pantry:   {bg:"#FF9F1C22",border:"#FF9F1C",text:"#FF9F1C"},
  Snacks:   {bg:"#FF6EB422",border:"#FF6EB4",text:"#FF6EB4"},
  Beverages:{bg:"#A855F722",border:"#A855F7",text:"#A855F7"},
  Frozen:   {bg:"#60A5FA22",border:"#60A5FA",text:"#60A5FA"},
  Other:    {bg:"#88888822",border:"#888888",text:"#888888"},
};

const SEED = [{"id":1009,"store":"Wegmans","date":"2026-03-02","total":181.00,"analysis":"","items":[{"name":"Fresh Cilantro","category":"Produce","price":1.19},{"name":"Wegmans Organic Ground Turkey","category":"Protein","price":9.19},{"name":"Wegmans Baby Spinach Salad","category":"Produce","price":2.59},{"name":"Wegmans Boneless Skinless Chicken Breast","category":"Protein","price":17.27},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":12.28},{"name":"Good Culture Cottage Cheese","category":"Dairy","price":4.59},{"name":"Applegate Organics Turkey Bacon","category":"Protein","price":7.29},{"name":"Wegmans Microwaveable Asparagus Tips","category":"Produce","price":4.59},{"name":"Broccoli Crowns","category":"Produce","price":7.29},{"name":"Wegmans Feta Cheese Crumbled","category":"Dairy","price":5.19},{"name":"Wegmans Onions Yellow","category":"Produce","price":2.29},{"name":"Fage Total Yogurt Nonfat Greek","category":"Dairy","price":1.99},{"name":"Wegmans Mini Seedless Cucumbers","category":"Produce","price":3.49},{"name":"Wegmans Lemon Sparkling Water 12pk","category":"Beverages","price":5.19},{"name":"Wegmans Chicken Thighs Boneless","category":"Protein","price":10.45},{"name":"Wegmans Liquid Egg Whites","category":"Dairy","price":6.89},{"name":"Wegmans Organic Ginger","category":"Produce","price":3.49},{"name":"Blueberries","category":"Produce","price":5.19},{"name":"Green Squash Zucchini","category":"Produce","price":3.30},{"name":"Wegmans Campari Cocktail Tomatoes","category":"Produce","price":4.99},{"name":"Serrano Peppers","category":"Produce","price":0.78},{"name":"Wegmans Pitted Kalamata Olives","category":"Pantry","price":4.09},{"name":"Wegmans Grade AA Large Eggs","category":"Dairy","price":3.49},{"name":"Wegmans Mixed Peppers 6 Pack","category":"Produce","price":8.09},{"name":"Wegmans Potatoes Baby Medley","category":"Produce","price":5.79}]},{"id":1001,"store":"Wegmans","date":"2026-03-02","total":180.31,"analysis":"","items":[{"name":"Green Squash Zucchini","category":"Produce","price":1.38},{"name":"Wegmans Grade AA Large Eggs","category":"Dairy","price":3.49},{"name":"Wegmans Organic Turkey Breast","category":"Protein","price":7.61},{"name":"Good Culture Cottage Cheese","category":"Dairy","price":4.59},{"name":"Kodiak Power Waffles","category":"Pantry","price":6.89},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":21.96},{"name":"Wegmans Organic Mini Cucumbers","category":"Produce","price":4.59},{"name":"Extra Large Green Peppers","category":"Produce","price":1.36},{"name":"Wegmans Granny Smith Apples","category":"Produce","price":5.79},{"name":"Strawberries","category":"Produce","price":6.39},{"name":"Tru Fru Strawberries Chocolate","category":"Snacks","price":8.99},{"name":"Wegmans Ground Chicken 3 Pack","category":"Protein","price":13.79},{"name":"Wegmans Organic Chicken Sausage","category":"Protein","price":8.09},{"name":"Wegmans Avocados Bagged","category":"Produce","price":3.49},{"name":"Wegmans Lemon Sparkling Water 12pk","category":"Beverages","price":5.19},{"name":"Wegmans Frozen Mukimame Soybeans","category":"Frozen","price":2.89},{"name":"Wegmans Organic Sweet Potatoes","category":"Produce","price":4.59},{"name":"Wegmans Spicy Red Pepper Hummus","category":"Pantry","price":3.49},{"name":"Wegmans Tzatziki Dip","category":"Pantry","price":4.09},{"name":"Mina Harissa Sauce","category":"Pantry","price":8.09},{"name":"Wegmans Asian Slaw","category":"Produce","price":4.09},{"name":"Polar Chestnuts Sliced Water","category":"Pantry","price":2.89},{"name":"Polar Bamboo Shoots","category":"Pantry","price":2.89},{"name":"Applegate Organics Turkey Bacon","category":"Protein","price":7.29},{"name":"Wegmans Broccoletti","category":"Produce","price":6.09},{"name":"Wegmans Organic Ginger","category":"Produce","price":3.49},{"name":"Bulk Garlic","category":"Produce","price":1.51},{"name":"Josephs Pita Bread","category":"Pantry","price":2.89}]},{"id":1008,"store":"Wegmans","date":"2026-02-21","total":130.07,"analysis":"","items":[{"name":"Wegmans Fresh Atlantic Salmon","category":"Protein","price":19.58},{"name":"Morton Bassett Red Chili Flakes","category":"Pantry","price":8.69},{"name":"Wegmans Cod Loin Iceland","category":"Protein","price":23.32},{"name":"Avocado","category":"Produce","price":2.38},{"name":"Traditional Medicinals Spearmint Tea","category":"Beverages","price":6.89},{"name":"Tru Fru Frozen Cherries Chocolate","category":"Frozen","price":8.99},{"name":"Mother In Laws Kimchi","category":"Pantry","price":11.49},{"name":"Wegmans Organic Mini Cucumbers","category":"Produce","price":4.59},{"name":"Tomatoes On-The-Vine","category":"Produce","price":3.15},{"name":"Granny Smith Apple","category":"Produce","price":5.49},{"name":"Wegmans Spaghetti Squash Halved","category":"Produce","price":4.59},{"name":"Wegmans Organic Frozen Blueberries","category":"Frozen","price":18.36}]},{"id":1007,"store":"Wegmans","date":"2026-02-18","total":208.60,"analysis":"","items":[{"name":"fairlife 2% Reduced Fat Milk","category":"Dairy","price":6.39},{"name":"Fage Total Yogurt Nonfat Greek","category":"Dairy","price":9.19},{"name":"MorningStar Farms Grillers Burgers","category":"Frozen","price":8.89},{"name":"Wegmans Organic Sourdough Bread","category":"Pantry","price":6.89},{"name":"Wegmans Chicken Thighs Boneless","category":"Protein","price":20.18},{"name":"Wegmans Ground Chicken","category":"Protein","price":12.38},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":14.18},{"name":"Wegmans Organic Chicken Sausage","category":"Protein","price":8.09},{"name":"Wegmans Liquid Egg Whites","category":"Dairy","price":6.89},{"name":"Wegmans Grade AA Large Eggs","category":"Dairy","price":3.49},{"name":"Wegmans Microwaveable Asparagus","category":"Produce","price":4.09},{"name":"Wegmans Organic Baby Spinach","category":"Produce","price":3.79},{"name":"Wegmans Mini Seedless Cucumbers","category":"Produce","price":3.49},{"name":"Wegmans Onions Red","category":"Produce","price":3.49},{"name":"Wegmans Peeled Garlic Family Pack","category":"Produce","price":5.79},{"name":"Wegmans Limes Bagged","category":"Produce","price":4.59},{"name":"Wegmans Lemons Bagged","category":"Produce","price":5.79},{"name":"Iceberg Lettuce","category":"Produce","price":2.29},{"name":"Good Culture Cottage Cheese","category":"Dairy","price":4.59},{"name":"Wegmans Lemon Sparkling Water 12pk","category":"Beverages","price":4.19},{"name":"Cocojune Yogurt Vanilla Cinnamon","category":"Dairy","price":2.99},{"name":"Wegmans Broccoli Cauliflower Florets","category":"Produce","price":3.29},{"name":"Wegmans Sweet Potato Microwaveable","category":"Produce","price":1.79},{"name":"Wegmans Baby Gold Potatoes","category":"Produce","price":9.18},{"name":"Blackberries Family Pack","category":"Produce","price":6.89},{"name":"Fresh Ginger","category":"Produce","price":1.23}]},{"id":1002,"store":"Wegmans","date":"2025-12-07","total":150.04,"analysis":"","items":[{"name":"Wegmans Ground Chicken 3 Pack","category":"Protein","price":13.79},{"name":"Fresh Cilantro","category":"Produce","price":1.19},{"name":"Wegmans Limes Bagged","category":"Produce","price":4.59},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":24.21},{"name":"Wegmans Mixed Peppers 6 Pack","category":"Produce","price":8.09},{"name":"Wegmans Orzo Pasta","category":"Pantry","price":1.19},{"name":"Wegmans Chicken Sausage Sundried Tomato","category":"Protein","price":6.39},{"name":"BelGioioso Parmesan Cheese Grated","category":"Dairy","price":5.79},{"name":"Wegmans Baby Spinach Salad","category":"Produce","price":2.59},{"name":"Bobs Red Mill Potato Starch","category":"Pantry","price":6.39},{"name":"Wegmans Microwaveable Asparagus","category":"Produce","price":4.09},{"name":"Wegmans Baby Gold Potatoes","category":"Produce","price":4.59},{"name":"Veggies Made Great Chocolate Muffins","category":"Snacks","price":8.09},{"name":"Wegmans Granny Smith Apples","category":"Produce","price":6.89},{"name":"Wegmans Thai Chili Chopped Salad Kit","category":"Produce","price":4.59},{"name":"Wegmans Chicken Thighs Boneless","category":"Protein","price":10.17},{"name":"Wegmans Baby Corn","category":"Produce","price":3.79},{"name":"Ortega Taco Seasoning","category":"Pantry","price":1.49},{"name":"McCormick Taco Seasoning Mix","category":"Pantry","price":3.58},{"name":"Josephs Mini Oat Bran Pita Bread","category":"Pantry","price":4.09},{"name":"Wegmans Peeled Garlic Family Pack","category":"Produce","price":5.79}]},{"id":1003,"store":"Wegmans","date":"2026-01-04","total":162.98,"analysis":"","items":[{"name":"Wegmans Baby Spinach Salad","category":"Produce","price":2.59},{"name":"Wegmans Ground Chicken","category":"Protein","price":6.19},{"name":"Wegmans Bagged Clementines","category":"Produce","price":6.89},{"name":"Wegmans Lemons Bagged","category":"Produce","price":5.79},{"name":"Tru Fru Frozen Cherries Chocolate","category":"Frozen","price":8.99},{"name":"Wegmans Clementines Bagged","category":"Produce","price":4.59},{"name":"Wegmans Organic Extra Firm Tofu","category":"Protein","price":2.69},{"name":"Wegmans Organic Mixed Peppers","category":"Produce","price":7.49},{"name":"Baby Bok Choy","category":"Produce","price":7.76},{"name":"Wegmans Organic Caprese Chicken Sausage","category":"Protein","price":8.09},{"name":"Wegmans Organic Peeled Garlic","category":"Produce","price":4.59},{"name":"Wegmans Organic Beets","category":"Produce","price":4.09},{"name":"Method All-Purpose Cleaner","category":"Other","price":6.09},{"name":"Kettle Fire Turmeric Ginger Bone Broth","category":"Pantry","price":8.69},{"name":"Wegmans Chocolate Chip Cookies","category":"Snacks","price":4.09},{"name":"Wegmans Organic Mini Avocados","category":"Produce","price":6.89},{"name":"Wegmans Organic Mini Cucumbers","category":"Produce","price":4.59},{"name":"Wegmans Organic Sweet Potatoes","category":"Produce","price":4.59},{"name":"Red Onions","category":"Produce","price":8.34},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":7.61},{"name":"Pete Gerrys Organic Eggs","category":"Dairy","price":8.09},{"name":"Wegmans Lemon Sparkling Water 12pk","category":"Beverages","price":5.19}]},{"id":1004,"store":"Wegmans","date":"2026-01-13","total":125.52,"analysis":"","items":[{"name":"Wegmans Onions Red","category":"Produce","price":3.49},{"name":"Wegmans Southwest Chopped Salad Kit","category":"Produce","price":4.59},{"name":"Wegmans Organic Extra Firm Tofu","category":"Protein","price":2.69},{"name":"Wel-Pac Edamame Shelled","category":"Frozen","price":5.79},{"name":"Blackberries","category":"Produce","price":4.09},{"name":"Wegmans Pure Ground Black Pepper","category":"Pantry","price":5.19},{"name":"Wegmans Baby Spinach Salad","category":"Produce","price":2.59},{"name":"Wegmans Granny Smith Apples","category":"Produce","price":6.89},{"name":"POM Wonderful Pomegranate Arils","category":"Produce","price":6.89},{"name":"Base Culture Simply Bread","category":"Pantry","price":9.19},{"name":"Good Culture Cottage Cheese","category":"Dairy","price":4.59},{"name":"Marine Treasures Argentine Red Shrimp","category":"Protein","price":10.99},{"name":"Wegmans Organic Ground Chicken","category":"Protein","price":8.09},{"name":"Hals New York Lemon Seltzer","category":"Beverages","price":6.89},{"name":"Yams Sweet Potatoes","category":"Produce","price":5.03},{"name":"Wegmans Cole Slaw","category":"Produce","price":2.39},{"name":"Fresh Ginger","category":"Produce","price":2.13},{"name":"Broccoli Crowns","category":"Produce","price":3.34},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":13.14}]},{"id":1005,"store":"Wegmans","date":"2026-01-24","total":171.98,"analysis":"","items":[{"name":"Wegmans Organic Unsalted Butter","category":"Dairy","price":7.49},{"name":"Fage Total Yogurt Nonfat Greek","category":"Dairy","price":9.19},{"name":"Organic Bananas Bunch","category":"Produce","price":2.77},{"name":"Wegmans Fresh Atlantic Salmon Fillet","category":"Protein","price":22.48},{"name":"Wegmans Chicken Thighs Boneless","category":"Protein","price":9.17},{"name":"Wegmans Cleaned Cut Leeks","category":"Produce","price":4.59},{"name":"Wegmans Onions Red","category":"Produce","price":3.49},{"name":"Wegmans Organic Carrots","category":"Produce","price":1.79},{"name":"Wegmans Microwaveable Asparagus","category":"Produce","price":4.09},{"name":"Wegmans Organic Sweet Potatoes","category":"Produce","price":4.59},{"name":"Wegmans Boneless Skinless Chicken Breast","category":"Protein","price":10.27},{"name":"Wegmans Granny Smith Apples","category":"Produce","price":6.89},{"name":"Koia Shake Cold Brew Coffee","category":"Beverages","price":4.99},{"name":"Koia Protein Cacao Bean Shake","category":"Beverages","price":4.99},{"name":"Wegmans Amore Orecchiette Pasta","category":"Pantry","price":5.79},{"name":"Cocojune Cultured Coconut Yogurt","category":"Dairy","price":5.78},{"name":"Fresh Nappa Cabbage","category":"Produce","price":9.04},{"name":"Wegmans Baby Medley Potatoes","category":"Produce","price":4.59},{"name":"Long Hot Green Pepper","category":"Produce","price":2.16},{"name":"Wegmans Mini Sweet Peppers","category":"Produce","price":8.09},{"name":"Empire Kosher Ground Turkey","category":"Protein","price":6.39}]},{"id":1006,"store":"Wegmans","date":"2026-02-01","total":198.82,"analysis":"","items":[{"name":"Wegmans Boneless Skinless Chicken Breast","category":"Protein","price":7.92},{"name":"Landhaus Butterkase Cheese","category":"Dairy","price":9.86},{"name":"Wegmans Chicken Thighs Boneless","category":"Protein","price":8.16},{"name":"Wegmans Fresh Atlantic Salmon","category":"Protein","price":19.58},{"name":"Wegmans Microwaveable Asparagus","category":"Produce","price":4.09},{"name":"Wegmans Potatoes Baby Medley","category":"Produce","price":5.79},{"name":"Wegmans Organic Toasted Sesame Salad Kit","category":"Produce","price":5.79},{"name":"Wegmans Lemons Bagged","category":"Produce","price":5.79},{"name":"Wegmans Sweet Potato Microwaveable","category":"Produce","price":3.58},{"name":"Wegmans Organic White Rice Noodles","category":"Pantry","price":3.49},{"name":"Wegmans Cilantro Jalapeno Hummus","category":"Pantry","price":2.79},{"name":"Good Culture Cottage Cheese","category":"Dairy","price":4.59},{"name":"Blackberries Family Pack","category":"Produce","price":6.89},{"name":"Serrano Peppers","category":"Produce","price":1.97},{"name":"Fresh Cilantro","category":"Produce","price":1.19},{"name":"Wegmans Organic Sourdough Bread","category":"Pantry","price":6.89},{"name":"Wegmans Organic Baby Spinach","category":"Produce","price":3.79},{"name":"Wegmans Oven Roasted Turkey Breast","category":"Protein","price":8.51},{"name":"Wegmans Clementines Bagged","category":"Produce","price":4.59},{"name":"Nature Valley Sweet Salty Granola Bars","category":"Snacks","price":4.59},{"name":"Ore-Ida Crispy Hash Brown Patties","category":"Frozen","price":5.29},{"name":"Wegmans Mild Italian Chicken Sausage","category":"Protein","price":6.39},{"name":"Wegmans Organic Uncured Turkey Bacon","category":"Protein","price":8.39},{"name":"MorningStar Farms Chikn Nuggets","category":"Frozen","price":10.39},{"name":"Wegmans Organic Sweet Basil","category":"Produce","price":5.79},{"name":"Wegmans Garlic 5 Count Family Pack","category":"Produce","price":1.79},{"name":"Wegmans Mini Seedless Cucumbers","category":"Produce","price":3.49}]}];

function useIsMobile() {
  const [mobile, setMobile] = useState(window.innerWidth < 640);
  useEffect(() => {
    const h = () => setMobile(window.innerWidth < 640);
    window.addEventListener("resize", h);
    return () => window.removeEventListener("resize", h);
  }, []);
  return mobile;
}

function Pill({ label }) {
  const c = TAG[label] || TAG["Other"];
  return <span style={{background:c.bg,border:\`1px solid \${c.border}\`,color:c.text,borderRadius:20,padding:"2px 10px",fontSize:11,fontWeight:700,letterSpacing:0.5}}>{label}</span>;
}

function btnStyle(bg, color="#000") {
  return {background:bg,color,border:\`2px solid \${bg}\`,borderRadius:12,padding:"10px 20px",fontWeight:700,fontSize:14,cursor:"pointer",letterSpacing:0.3};
}

async function callClaude(messages, system) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:1000,system,messages})
  });
  const d = await res.json();
  return d.content?.[0]?.text || "";
}

async function callClaudeSearch(messages, system) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:1000,system,tools:[{type:"web_search_20250305",name:"web_search"}],messages})
  });
  const d = await res.json();
  return d.content?.find(b=>b.type==="text")?.text || "";
}

async function fileToBase64(file) {
  return new Promise((res,rej) => { const r=new FileReader(); r.onload=()=>res(r.result.split(",")[1]); r.onerror=()=>rej(new Error("fail")); r.readAsDataURL(file); });
}

async function parseReceipt(input, store, isFile) {
  const sys = \`You are a grocery receipt parser. Extract every line item. Return ONLY valid JSON with no markdown, no backticks, no extra text before or after.
Format: {"date":"YYYY-MM-DD","store":"\${store}","total":0.00,"items":[{"name":"Item Name","category":"Protein|Produce|Dairy|Pantry|Snacks|Beverages|Frozen|Other","price":0.00,"quantity":1}]}\`;
  let msgs;
  if (isFile) {
    const b64 = await fileToBase64(input);
    const isPdf = input.type === "application/pdf" || input.name?.endsWith(".pdf");
    if (isPdf) {
      // PDFs: send as document type
      msgs = [{role:"user",content:[
        {type:"document",source:{type:"base64",media_type:"application/pdf",data:b64}},
        {type:"text",text:"This is a grocery receipt PDF. Extract all line items and return JSON only."}
      ]}];
    } else {
      // Images
      const mt = input.type || "image/jpeg";
      msgs = [{role:"user",content:[
        {type:"image",source:{type:"base64",media_type:mt,data:b64}},
        {type:"text",text:"This is a grocery receipt image. Extract all line items and return JSON only."}
      ]}];
    }
  } else {
    msgs = [{role:"user",content:\`Parse this grocery receipt and return JSON only:\\n\\n\${input}\`}];
  }
  const raw = await callClaude(msgs, sys);
  // Extract JSON from response — find first { to last }
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start === -1 || end === -1) throw new Error("No JSON in response: " + raw.slice(0,200));
  let jsonStr = raw.slice(start, end + 1);
  // Fix unescaped apostrophes inside JSON string values (e.g. Pete & Gerry's)
  // Replace curly/smart quotes with straight quotes
  jsonStr = jsonStr.replace(/[‘’]/g, "\\'").replace(/[“”]/g, '\\"');
  try {
    return JSON.parse(jsonStr);
  } catch(parseErr) {
    // Ask Claude to fix its own JSON
    const fixPrompt = \`This JSON has a syntax error. Fix it and return ONLY valid JSON, nothing else:\\n\${jsonStr}\`;
    const fixed = await callClaude([{role:"user",content:fixPrompt}], "You are a JSON fixer. Return only valid JSON.");
    const fs = fixed.indexOf("{"); const fe = fixed.lastIndexOf("}");
    if (fs === -1 || fe === -1) throw new Error("Could not fix JSON");
    return JSON.parse(fixed.slice(fs, fe + 1));
  }
}

async function analyzeOrder(order, allOrders) {
  const others = allOrders.filter(o=>o.id!==order.id);
  const avg = others.length>0?others.reduce((s,o)=>s+o.total,0)/others.length:null;
  const ctx = avg?\`Average spend (excluding this): $\${avg.toFixed(2)}.\`:"This is the first order.";
  const prompt = \`\${ctx}\\n\\nOrder from \${order.store} on \${order.date}: $\${order.total.toFixed(2)}\\nItems:\\n\${order.items.map(i=>\`- \${i.name} (\${i.category}): $\${i.price.toFixed(2)}\`).join("\\n")}\\n\\nWrite a SHORT, friendly 2-3 sentence analysis. Be specific about actual items. Keep it casual.\`;
  return callClaude([{role:"user",content:prompt}], "You are a friendly grocery budget analyst. Be short and specific.");
}

async function estimateMealPlan(text, history) {
  const hist = history.length>0?\`Historical prices:\\n\${history.flatMap(o=>o.items.map(i=>\`\${i.name} at \${o.store}: $\${i.price.toFixed(2)}\`)).join("\\n")}\`:"No history yet.";
  const raw = await callClaude([{role:"user",content:\`\${hist}\\n\\nMeal plan:\\n\${text}\\n\\nExtract all ingredients. Return ONLY JSON:\\n{"items":[{"name":"","category":"","estimated_price":0.00,"from_history":true,"needs_lookup":false,"preferred_store":""}],"recommended_store":"","store_reasoning":""}\`}], "You are a grocery cost estimator. Return only valid JSON.");
  const parsed = JSON.parse(raw.replace(/\`\`\`json|\`\`\`/g,"").trim());
  for (const item of parsed.items.filter(i=>i.needs_lookup)) {
    try {
      const r = await callClaudeSearch([{role:"user",content:\`Current price of "\${item.name}" at \${parsed.recommended_store||"Wegmans"}? Just the dollar amount.\`}], "Return only a price like: 4.99");
      const m = r.match(/\\d+\\.\\d{2}|\\d+/);
      if (m) { item.estimated_price=parseFloat(m[0]); item.from_search=true; item.needs_lookup=false; }
    } catch(e) { item.estimated_price=item.estimated_price||3.99; }
  }
  return parsed;
}

function UploadZone({ onFile, onText, label, accept, placeholder }) {
  const [dragging,setDragging]=useState(false);
  const [text,setText]=useState("");
  const ref=useRef();
  return (
    <div style={{display:"flex",flexDirection:"column",gap:12}}>
      <div onClick={()=>ref.current.click()}
        onDragOver={(e)=>{e.preventDefault();setDragging(true);}}
        onDragLeave={()=>setDragging(false)}
        onDrop={(e)=>{e.preventDefault();setDragging(false);const f=e.dataTransfer.files[0];if(f)onFile(f);}}
        style={{border:\`2px dashed \${dragging?C.lime:C.border}\`,borderRadius:16,padding:"28px 20px",textAlign:"center",cursor:"pointer",background:dragging?"#C8F13508":"transparent"}}>
        <div style={{fontSize:32,marginBottom:8}}>📎</div>
        <div style={{color:C.text,fontWeight:600,fontSize:14}}>{label}</div>
        <div style={{color:C.muted,fontSize:12,marginTop:4}}>PDF, image, or screenshot</div>
        <input ref={ref} type="file" accept={accept} style={{display:"none"}} onChange={(e)=>{if(e.target.files[0])onFile(e.target.files[0]);}} />
      </div>
      <div style={{textAlign:"center",color:C.muted,fontSize:12}}>— or paste text below —</div>
      <textarea value={text} onChange={(e)=>setText(e.target.value)} placeholder={placeholder} rows={5}
        style={{background:C.card,border:\`1px solid \${C.border}\`,borderRadius:12,color:C.text,padding:"12px 16px",fontSize:13,resize:"vertical",fontFamily:"monospace",outline:"none",lineHeight:1.6}} />
      {text.trim() && <button onClick={()=>{onText(text);setText("");}} style={btnStyle(C.lime,"#000")}>Process Text →</button>}
    </div>
  );
}

export default function App() {
  const isMobile = useIsMobile();
  const [tab,setTab]=useState("dashboard");
  const [orders,setOrders]=useState([]);
  const [budget,setBudget]=useState(DEFAULT_BUDGET);
  const [editingBudget,setEditingBudget]=useState(false);
  const [budgetInput,setBudgetInput]=useState(String(DEFAULT_BUDGET));
  const [loading,setLoading]=useState(false);
  const [loadingMsg,setLoadingMsg]=useState("");
  const [expanded,setExpanded]=useState(null);
  const [store,setStore]=useState("Wegmans");
  const [estimate,setEstimate]=useState(null);
  const [toast,setToast]=useState(null);
  const [insights,setInsights]=useState(null);
  const [insightsLoading,setInsightsLoading]=useState(false);
  const [donutRange,setDonutRange]=useState("3mo"); // "1mo" | "3mo" | "all"
  const [orderDate,setOrderDate]=useState(() => new Date().toISOString().slice(0,10));
  const [confirmDelete,setConfirmDelete]=useState(null); // order id to confirm delete

  const SEED_VERSION = "v3"; // bump this to force re-seed with corrected data

  useEffect(()=>{
    (async()=>{
      let loaded=false;
      // Check seed version — if outdated, force re-seed with corrected dates
      try {
        const ver = await window.storage.get("seed_version");
        if (ver?.value === SEED_VERSION) {
          const r=await window.storage.get(STORAGE_KEY);
          if(r?.value){const p=JSON.parse(r.value);if(p.length>0){setOrders(p);loaded=true;}}
        }
      } catch(e){}
      if(!loaded){
        setOrders(SEED);
        try{await window.storage.set(STORAGE_KEY,JSON.stringify(SEED));}catch(e){}
        try{await window.storage.set("seed_version",SEED_VERSION);}catch(e){}
      }
      try { const r=await window.storage.get(BUDGET_KEY); if(r?.value){const n=parseFloat(r.value);setBudget(n);setBudgetInput(String(n));} } catch(e){}
      try { const r=await window.storage.get(INSIGHTS_KEY); if(r?.value)setInsights(JSON.parse(r.value)); } catch(e){}
    })();
  },[]);

  const save = async(o)=>{ setOrders(o); try{await window.storage.set(STORAGE_KEY,JSON.stringify(o));}catch(e){} };
  const saveBudget = async(v)=>{ const n=parseFloat(v); if(!isNaN(n)&&n>0){setBudget(n);try{await window.storage.set(BUDGET_KEY,String(n));}catch(e){}} setEditingBudget(false); };
  const showToast = (msg,type="success")=>{ setToast({msg,type}); setTimeout(()=>setToast(null),3000); };

  const deleteOrder = async(id)=>{
    const updated = orders.filter(o=>o.id!==id);
    await save(updated);
    setConfirmDelete(null);
    setExpanded(null);
    showToast("Order removed.");
  };

  const generateInsights = async()=>{
    if(!orders.length) return;
    setInsightsLoading(true);
    const avg=orders.reduce((s,o)=>s+o.total,0)/orders.length;
    const summary=orders.map(o=>({date:o.date,store:o.store,total:o.total,items:o.items.map(i=>\`\${i.name}($\${i.price.toFixed(2)})\`).join(",")}));
    const prompt=\`You are a grocery spending analyst. Order history:\\n\${JSON.stringify(summary,null,2)}\\n\\nAverage: $\${avg.toFixed(2)}\\n\\nReturn ONLY a JSON array of 4-5 insight objects. No markdown, no backticks.\\n[\\n  {"emoji":"🐟","title":"Short title","detail":"1-2 sentences with specific items/prices and a concrete suggestion."}\\n]\\nFocus on: spending drivers, volatile items, one-offs vs recurring, budget trends, easy wins.\`;
    try {
      const res=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({model:"claude-sonnet-4-20250514",max_tokens:1000,messages:[{role:"user",content:prompt}]})});
      const d=await res.json();
      const text=d.content?.[0]?.text||"";
      const parsed=JSON.parse(text.replace(/\`\`\`json|\`\`\`/g,"").trim());
      setInsights(parsed);
      try{await window.storage.set(INSIGHTS_KEY,JSON.stringify(parsed));}catch(e){}
    } catch(e){ showToast("Couldn't generate insights.","error"); }
    setInsightsLoading(false);
  };

  const handleFile=async(file)=>{
    setLoading(true);setLoadingMsg("Parsing receipt...");
    try {
      const p=await parseReceipt(file,store,true);
      const finalDate = orderDate || p.date;
      setLoadingMsg("Analyzing spend...");
      const id=Date.now();
      const order={...p,id,date:finalDate};
      const analysis=await analyzeOrder(order,[...orders,order]);
      const updated=[...orders,{...order,analysis}].sort((a,b)=>new Date(b.date)-new Date(a.date));
      await save(updated);setExpanded(id);setTab("dashboard");showToast("Receipt added! 🛒");
    } catch(e){ console.error("Parse error:",e); showToast("Parse failed: " + (e.message||"unknown error").slice(0,60), "error"); }
    setLoading(false);
  };

  const handleText=async(text)=>{
    setLoading(true);setLoadingMsg("Parsing receipt...");
    try {
      const p=await parseReceipt(text,store,false);
      const finalDate = orderDate || p.date;
      setLoadingMsg("Analyzing spend...");
      const id=Date.now();
      const order={...p,id,date:finalDate};
      const analysis=await analyzeOrder(order,[...orders,order]);
      const updated=[...orders,{...order,analysis}].sort((a,b)=>new Date(b.date)-new Date(a.date));
      await save(updated);setExpanded(id);setTab("dashboard");showToast("Receipt added! 🛒");
    } catch(e){ showToast("Couldn't parse receipt.","error"); }
    setLoading(false);
  };

  const handleMealPlan=async(text)=>{
    setLoading(true);setLoadingMsg("Estimating costs...");
    try { const r=await estimateMealPlan(text,orders);setEstimate(r);showToast("Estimate ready! 🎯"); }
    catch(e){ showToast("Couldn't process meal plan.","error"); }
    setLoading(false);
  };

  // Derived
  const now=new Date();
  const thisMonth=orders.filter(o=>{ const d=new Date(o.date); return d.getMonth()===now.getMonth()&&d.getFullYear()===now.getFullYear(); });
  const thisMonthSpend=thisMonth.reduce((s,o)=>s+o.total,0);
  const budgetLeft=budget-thisMonthSpend;
  const budgetPct=Math.min(thisMonthSpend/budget,1);
  const budgetColor=budgetPct>0.9?C.coral:budgetPct>0.7?C.orange:C.lime;
  const avg=orders.length>0?orders.reduce((s,o)=>s+o.total,0)/orders.length:0;
  const lastMonth=orders.filter(o=>{ const d=new Date(o.date); return d.getMonth()===(now.getMonth()-1+12)%12&&d.getFullYear()===(now.getMonth()===0?now.getFullYear()-1:now.getFullYear()); });
  const lastMonthSpend=lastMonth.reduce((s,o)=>s+o.total,0);
  const momDiff=lastMonthSpend>0?((thisMonthSpend-lastMonthSpend)/lastMonthSpend*100):null;

  // Donut data filtered by range
  const donutOrders = orders.filter(o=>{
    const d=new Date(o.date);
    if(donutRange==="1mo") return d>=new Date(now.getFullYear(),now.getMonth(),1);
    if(donutRange==="3mo") return d>=new Date(now.getFullYear(),now.getMonth()-3,1);
    return true;
  });
  const catTotals={};
  donutOrders.forEach(o=>o.items.forEach(i=>{ catTotals[i.category]=(catTotals[i.category]||0)+i.price; }));
  const donutData=Object.entries(catTotals).map(([name,value])=>({name,value:parseFloat(value.toFixed(2))})).sort((a,b)=>b.value-a.value);

  // Aggregate orders by month for trend chart
  const chartData = (() => {
    const monthly = {};
    orders.forEach(o => {
      const key = o.date?.slice(0,7); // "YYYY-MM"
      if (!key) return;
      if (!monthly[key]) monthly[key] = { month: key, total: 0, orders: 0 };
      monthly[key].total += o.total;
      monthly[key].orders += 1;
    });
    return Object.values(monthly)
      .sort((a,b) => a.month.localeCompare(b.month))
      .map(m => {
        const [yr, mo] = m.month.split("-");
        const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
        const label = \`\${monthNames[parseInt(mo)-1]}'\${yr.slice(2)}\`;
        return {
          date: label,
          total: parseFloat(m.total.toFixed(2)),
          orders: m.orders,
          month: m.month,
        };
      });
  })();

  const DonutTooltip=({active,payload})=>{
    if(!active||!payload?.length) return null;
    const d=payload[0];
    const color=DONUT_COLORS[d.name]||"#888";
    return (
      <div style={{background:"#1A1A2E",border:\`2px solid \${color}\`,borderRadius:10,padding:"8px 14px",boxShadow:"0 4px 20px #00000066"}}>
        <div style={{color,fontWeight:800,fontSize:13}}>{d.name}</div>
        <div style={{color:"#F0F0FF",fontWeight:700,fontSize:16,marginTop:2}}>\${d.value.toFixed(2)}</div>
        <div style={{color:"#8888AA",fontSize:11,marginTop:1}}>{((d.value/donutOrders.reduce((s,o)=>s+o.items.reduce((ss,i)=>ss+i.price,0),0))*100).toFixed(0)}% of spend</div>
      </div>
    );
  };

  const LineTooltip=({active,payload})=>{
    const pt=payload?.find(p=>p.payload?.month);
    if(!active||!pt) return null;
    const d=pt.payload;
    const over = d.total > budget;
    return (
      <div style={{background:"#1A1A2E",border:\`1px solid \${over?C.coral:C.border}\`,borderRadius:10,padding:"10px 14px",boxShadow:"0 4px 20px #00000066"}}>
        <div style={{color:C.muted,fontSize:11,marginBottom:4}}>{d.month}</div>
        <div style={{color:over?C.coral:C.lime,fontWeight:700,fontSize:16}}>\${d.total.toFixed(2)}</div>
        <div style={{color:C.muted,fontSize:11,marginTop:3}}>{d.orders} order{d.orders!==1?"s":""} · budget \${budget}</div>
        {over && <div style={{color:C.coral,fontSize:11,fontWeight:700,marginTop:3}}>⚠️ +\${(d.total-budget).toFixed(2)} over</div>}
      </div>
    );
  };

  const rangeLabels={"1mo":"This Month","3mo":"3 Months","all":"All Time"};

  return (
    <div style={{minHeight:"100vh",background:C.bg,color:C.text,fontFamily:"'DM Sans','Nunito',system-ui,sans-serif",paddingBottom:80}}>
      <style>{\`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Space+Grotesk:wght@700;800&display=swap');
        *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
        ::-webkit-scrollbar{width:4px;} ::-webkit-scrollbar-track{background:\${C.bg};} ::-webkit-scrollbar-thumb{background:\${C.border};border-radius:3px;}
        button{transition:all 0.15s;} button:hover{opacity:0.85;}
        @keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
        @keyframes spin{to{transform:rotate(360deg);}}
        @keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.5;}}
      \`}</style>

      {/* Header */}
      <div style={{background:"linear-gradient(135deg,#1A1A2E 0%,#16213E 100%)",borderBottom:\`1px solid \${C.border}\`,padding:isMobile?"14px 16px 0":"18px 24px 0",position:"sticky",top:0,zIndex:100}}>
        <div style={{maxWidth:900,margin:"0 auto"}}>
          <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:14}}>
            <div style={{width:36,height:36,borderRadius:11,background:\`linear-gradient(135deg,\${C.lime},\${C.sky})\`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:18}}>🛒</div>
            <div>
              <div style={{fontFamily:"'Space Grotesk',sans-serif",fontSize:isMobile?18:21,fontWeight:800,letterSpacing:-0.5}}>Cart<span style={{color:C.lime}}>IQ</span></div>
              <div style={{fontSize:10,color:C.muted}}>your grocery brain 🧠</div>
            </div>
          </div>
          <div style={{display:"flex",gap:2}}>
            {[["dashboard","📊","Dashboard"],["add","➕","Add Receipt"],["estimate","🔮","Estimate"]].map(([id,icon,label])=>(
              <button key={id} onClick={()=>setTab(id)} style={{background:tab===id?C.lime:"transparent",color:tab===id?"#000":C.muted,border:"none",borderRadius:"10px 10px 0 0",padding:isMobile?"9px 14px":"9px 18px",fontWeight:700,fontSize:isMobile?12:13,cursor:"pointer",display:"flex",alignItems:"center",gap:5}}>
                <span>{icon}</span><span style={{display:isMobile&&tab!==id?"none":"inline"}}>{label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Toast */}
      {toast && (
        <div style={{position:"fixed",top:16,right:16,zIndex:999,background:toast.type==="error"?C.coral:C.lime,color:"#000",padding:"10px 18px",borderRadius:12,fontWeight:700,fontSize:13,animation:"fadeUp 0.3s ease",maxWidth:"calc(100vw - 32px)"}}>
          {toast.msg}
        </div>
      )}

      {/* Loading overlay */}
      {loading && (
        <div style={{position:"fixed",inset:0,background:"#0F0F1Aee",zIndex:200,display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",gap:16}}>
          <div style={{width:48,height:48,borderRadius:"50%",border:\`4px solid \${C.border}\`,borderTop:\`4px solid \${C.lime}\`,animation:"spin 0.8s linear infinite"}} />
          <div style={{color:C.muted,fontSize:14,animation:"pulse 1.5s infinite"}}>{loadingMsg}</div>
        </div>
      )}

      <div style={{maxWidth:900,margin:"0 auto",padding:isMobile?"16px 12px 0":"24px 24px 0"}}>

        {/* ── DASHBOARD ── */}
        {tab==="dashboard" && (
          <div style={{animation:"fadeUp 0.35s ease"}}>

            {/* Stats */}
            <div style={{display:"grid",gridTemplateColumns:isMobile?"1fr 1fr":"repeat(3,1fr)",gap:10,marginBottom:12}}>
              {[
                {label:"SPENT THIS MONTH",value:\`$\${thisMonthSpend.toFixed(2)}\`,sub:momDiff!==null?\`\${momDiff>0?"+":""}\${momDiff.toFixed(0)}% vs last month\`:"first month",subColor:momDiff>0?C.coral:C.lime},
                {label:"BUDGET LEFT",value:\`$\${budgetLeft.toFixed(2)}\`,sub:\`of $\${budget} budget\`,subColor:budgetLeft<0?C.coral:C.muted},
                {label:"AVG PER ORDER",value:\`$\${avg.toFixed(2)}\`,sub:\`\${orders.length} total orders\`,subColor:C.muted,fullWidth:isMobile},
              ].map((s,i)=>(
                <div key={i} style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"12px 14px":"16px 18px",gridColumn:s.fullWidth?"1 / -1":"auto"}}>
                  <div style={{fontSize:9,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:4}}>{s.label}</div>
                  <div style={{fontSize:isMobile?20:24,fontWeight:800,fontFamily:"'Space Grotesk',sans-serif",color:C.text}}>{s.value}</div>
                  <div style={{fontSize:11,color:s.subColor,marginTop:2}}>{s.sub}</div>
                </div>
              ))}
            </div>

            {/* Budget bar */}
            <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"12px 14px":"14px 18px",marginBottom:12}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8}}>
                <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1}}>MONTHLY BUDGET</div>
                {editingBudget?(
                  <div style={{display:"flex",gap:6,alignItems:"center"}}>
                    <input value={budgetInput} onChange={(e)=>setBudgetInput(e.target.value)} onKeyDown={(e)=>{if(e.key==="Enter")saveBudget(budgetInput);if(e.key==="Escape")setEditingBudget(false);}}
                      style={{background:C.bg,border:\`1px solid \${C.lime}\`,borderRadius:8,color:C.text,padding:"4px 10px",fontSize:14,width:80,outline:"none"}} autoFocus />
                    <button onClick={()=>saveBudget(budgetInput)} style={{background:C.lime,color:"#000",border:"none",borderRadius:8,padding:"6px 12px",fontWeight:700,fontSize:13,cursor:"pointer"}}>✓</button>
                    <button onClick={()=>setEditingBudget(false)} style={{background:C.border,color:C.text,border:"none",borderRadius:8,padding:"6px 12px",fontWeight:700,fontSize:13,cursor:"pointer"}}>✕</button>
                  </div>
                ):(
                  <button onClick={()=>setEditingBudget(true)} style={{background:"transparent",border:"none",color:C.muted,fontSize:12,cursor:"pointer",padding:"4px 8px"}}>✏️ edit</button>
                )}
              </div>
              <div style={{background:C.bg,borderRadius:8,height:10,overflow:"hidden"}}>
                <div style={{height:"100%",width:\`\${budgetPct*100}%\`,background:\`linear-gradient(90deg,\${budgetColor},\${budgetColor}88)\`,borderRadius:8,transition:"width 0.5s ease"}} />
              </div>
              <div style={{display:"flex",justifyContent:"space-between",marginTop:6}}>
                <span style={{fontSize:11,color:budgetColor,fontWeight:700}}>{(budgetPct*100).toFixed(0)}% used</span>
                <span style={{fontSize:11,color:C.muted}}>\${budget} budget</span>
              </div>
            </div>

            {/* Charts — stack on mobile */}
            <div style={{display:"grid",gridTemplateColumns:isMobile?"1fr":"1fr 1.7fr",gap:12,marginBottom:12}}>

              {/* Donut */}
              <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:"14px 16px"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:10}}>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1}}>BY CATEGORY</div>
                  {/* Range toggle */}
                  <div style={{display:"flex",gap:3,background:C.bg,borderRadius:8,padding:3}}>
                    {[["1mo","1M"],["3mo","3M"],["all","All"]].map(([key,label])=>(
                      <button key={key} onClick={()=>setDonutRange(key)} style={{background:donutRange===key?C.lime:"transparent",color:donutRange===key?"#000":C.muted,border:"none",borderRadius:6,padding:"3px 8px",fontWeight:700,fontSize:10,cursor:"pointer",transition:"all 0.15s"}}>
                        {label}
                      </button>
                    ))}
                  </div>
                </div>
                <div style={{fontSize:10,color:C.muted,marginBottom:8}}>{rangeLabels[donutRange]}</div>
                {donutData.length>0?(
                  <div>
                    <ResponsiveContainer width="100%" height={isMobile?200:190}>
                      <PieChart>
                        <Pie data={donutData} cx="50%" cy="45%" innerRadius={isMobile?55:50} outerRadius={isMobile?85:75} paddingAngle={3} dataKey="value">
                          {donutData.map((e,i)=><Cell key={i} fill={DONUT_COLORS[e.name]||"#888"} />)}
                        </Pie>
                        <Tooltip content={<DonutTooltip />} />
                        <Legend iconType="circle" iconSize={7} formatter={(v)=><span style={{fontSize:10,color:C.muted}}>{v}</span>} />
                      </PieChart>
                    </ResponsiveContainer>
                    {/* Top category bar */}
                    <div style={{marginTop:8,display:"flex",flexDirection:"column",gap:5}}>
                      {donutData.slice(0,3).map((d,i)=>{
                        const total=donutData.reduce((s,x)=>s+x.value,0);
                        const pct=(d.value/total*100).toFixed(0);
                        const color=DONUT_COLORS[d.name]||"#888";
                        return (
                          <div key={i}>
                            <div style={{display:"flex",justifyContent:"space-between",marginBottom:3}}>
                              <span style={{fontSize:11,color:color,fontWeight:700}}>{d.name}</span>
                              <span style={{fontSize:11,color:C.text,fontWeight:700}}>\${d.value.toFixed(0)} <span style={{color:C.muted,fontWeight:400}}>({pct}%)</span></span>
                            </div>
                            <div style={{background:C.bg,borderRadius:4,height:4}}>
                              <div style={{height:"100%",width:\`\${pct}%\`,background:color,borderRadius:4,transition:"width 0.5s ease"}} />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ):<div style={{color:C.muted,fontSize:13,padding:20}}>No data for this period</div>}
              </div>

              {/* Trend */}
              <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:"14px 16px"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8}}>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1}}>SPEND TREND</div>
                  <div style={{fontSize:10,color:C.muted}}>monthly spend vs \${budget} budget</div>
                </div>
                <ResponsiveContainer width="100%" height={isMobile?180:220}>
                  <LineChart data={chartData} margin={{top:10,right:8,left:-15,bottom:0}}>
                    <CartesianGrid strokeDasharray="3 3" stroke={C.border} />
                    <XAxis dataKey="date" tick={{fill:C.muted,fontSize:9}} axisLine={false} tickLine={false} />
                    <YAxis tick={{fill:C.muted,fontSize:9}} axisLine={false} tickLine={false} tickFormatter={v=>\`$\${v}\`} />
                    <Tooltip content={<LineTooltip />} />
                    <Line type="monotone" dataKey={()=>budget} stroke={C.muted} strokeDasharray="5 5" strokeWidth={1} dot={false} legendType="none" activeDot={false} />
                    <Line type="monotone" dataKey="total" stroke={C.lime} strokeWidth={3}
                      dot={(props) => {
                        const over = props.payload?.total > budget;
                        return <circle key={props.index} cx={props.cx} cy={props.cy} r={5} fill={over?C.coral:C.lime} stroke="none" />;
                      }}
                      activeDot={{r:6,fill:C.lime}} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Insights */}
            <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"14px 14px":"18px 20px",marginBottom:12}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:insightsLoading||insights?14:0}}>
                <div>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1}}>✨ AI INSIGHTS</div>
                  {insights&&<div style={{fontSize:11,color:C.muted,marginTop:2}}>Based on your {orders.length} orders</div>}
                </div>
                <button onClick={generateInsights} disabled={insightsLoading} style={{background:insightsLoading?C.border:\`linear-gradient(135deg,\${C.purple},\${C.pink})\`,color:"#fff",border:"none",borderRadius:10,padding:"8px 14px",fontWeight:700,fontSize:12,cursor:insightsLoading?"default":"pointer",opacity:insightsLoading?0.7:1,minWidth:isMobile?100:120}}>
                  {insightsLoading?"Analyzing...":insights?"↺ Refresh":"✨ Generate"}
                </button>
              </div>
              {insightsLoading&&(
                <div style={{display:"flex",alignItems:"center",gap:10,padding:"8px 0"}}>
                  <div style={{width:18,height:18,borderRadius:"50%",border:\`3px solid \${C.border}\`,borderTop:\`3px solid \${C.purple}\`,animation:"spin 0.8s linear infinite",flexShrink:0}} />
                  <span style={{color:C.muted,fontSize:13,animation:"pulse 1.5s infinite"}}>Crunching your grocery data...</span>
                </div>
              )}
              {!insightsLoading&&insights&&(
                <div style={{display:"flex",flexDirection:"column",gap:8}}>
                  {insights.map((ins,i)=>(
                    <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start",padding:"10px 12px",borderRadius:12,background:\`linear-gradient(135deg,\${C.purple}10,\${C.pink}08)\`,border:\`1px solid \${C.purple}25\`,animation:\`fadeUp 0.3s ease \${i*0.07}s both\`}}>
                      <span style={{fontSize:18,flexShrink:0,marginTop:1}}>{ins.emoji}</span>
                      <div>
                        <div style={{fontWeight:700,fontSize:13,marginBottom:2,color:C.text}}>{ins.title}</div>
                        <div style={{fontSize:12,color:C.muted,lineHeight:1.6}}>{ins.detail}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
              {!insightsLoading&&!insights&&(
                <div style={{color:C.muted,fontSize:13,fontStyle:"italic",paddingTop:4}}>
                  Tap "Generate" for AI-powered takeaways from your grocery history.
                </div>
              )}
            </div>

            {/* Order history */}
            <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:10}}>ORDER HISTORY</div>
            {orders.length===0?(
              <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:40,textAlign:"center"}}>
                <div style={{fontSize:40,marginBottom:12}}>🧺</div>
                <div style={{fontWeight:700,fontSize:16,marginBottom:6}}>No orders yet!</div>
                <div style={{color:C.muted,fontSize:13,marginBottom:16}}>Add your first receipt to get started.</div>
                <button onClick={()=>setTab("add")} style={btnStyle(C.lime,"#000")}>Add First Receipt →</button>
              </div>
            ):(
              <div style={{display:"flex",flexDirection:"column",gap:8}}>
                {orders.map(o=>(
                  <div key={o.id} style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,overflow:"hidden",transition:"all 0.2s"}}>
                    <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",padding:isMobile?"12px 14px":"14px 18px"}}>
                      <div onClick={()=>setExpanded(expanded===o.id?null:o.id)} style={{display:"flex",alignItems:"center",gap:10,minWidth:0,flex:1,cursor:"pointer"}}>
                        <div style={{fontSize:20,flexShrink:0}}>🟢</div>
                        <div style={{minWidth:0}}>
                          <div style={{fontWeight:700,fontSize:isMobile?13:14,whiteSpace:"nowrap",overflow:"hidden",textOverflow:"ellipsis"}}>{o.store}</div>
                          <div style={{fontSize:11,color:C.muted}}>{o.date} · {o.items.length} items</div>
                        </div>
                      </div>
                      <div style={{display:"flex",alignItems:"center",gap:8,flexShrink:0}}>
                        <div onClick={()=>setExpanded(expanded===o.id?null:o.id)} style={{fontSize:isMobile?16:18,fontWeight:800,color:C.lime,fontFamily:"'Space Grotesk',sans-serif",cursor:"pointer"}}>\${o.total.toFixed(2)}</div>
                        <button onClick={(e)=>{e.stopPropagation();setConfirmDelete(o.id);}} style={{background:"transparent",border:\`1px solid \${C.border}\`,borderRadius:8,color:C.muted,fontSize:13,cursor:"pointer",padding:"4px 8px",lineHeight:1}} title="Remove order">🗑️</button>
                        <div onClick={()=>setExpanded(expanded===o.id?null:o.id)} style={{color:C.muted,fontSize:16,transform:expanded===o.id?"rotate(180deg)":"none",transition:"transform 0.2s",cursor:"pointer"}}>▾</div>
                      </div>
                    </div>
                    {expanded===o.id&&(
                      <div style={{borderTop:\`1px solid \${C.border}\`,padding:isMobile?"12px 14px":"14px 18px",animation:"fadeUp 0.2s ease"}}>
                        {o.analysis&&(
                          <div style={{background:C.bg,borderRadius:10,padding:"10px 12px",marginBottom:12,fontSize:13,color:C.muted,lineHeight:1.6,borderLeft:\`3px solid \${C.lime}\`}}>
                            {o.analysis}
                          </div>
                        )}
                        <div style={{display:"flex",flexDirection:"column",gap:6}}>
                          {o.items.map((item,i)=>(
                            <div key={i} style={{display:"flex",alignItems:"center",justifyContent:"space-between",gap:8}}>
                              <div style={{display:"flex",alignItems:"center",gap:6,minWidth:0}}>
                                <Pill label={item.category} />
                                <span style={{fontSize:12,color:C.text,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{item.name}</span>
                              </div>
                              <span style={{fontSize:13,fontWeight:700,color:C.lime,flexShrink:0}}>\${item.price.toFixed(2)}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Confirm delete modal */}
        {confirmDelete && (
          <div style={{position:"fixed",inset:0,background:"#0F0F1Acc",zIndex:300,display:"flex",alignItems:"center",justifyContent:"center",padding:16}}>
            <div style={{background:C.card,border:\`1px solid \${C.coral}\`,borderRadius:16,padding:"24px",maxWidth:320,width:"100%",textAlign:"center",animation:"fadeUp 0.2s ease"}}>
              <div style={{fontSize:28,marginBottom:12}}>🗑️</div>
              <div style={{fontWeight:700,fontSize:16,marginBottom:8}}>Remove this order?</div>
              <div style={{color:C.muted,fontSize:13,marginBottom:20}}>This can't be undone.</div>
              <div style={{display:"flex",gap:10,justifyContent:"center"}}>
                <button onClick={()=>setConfirmDelete(null)} style={{background:C.border,color:C.text,border:"none",borderRadius:10,padding:"10px 20px",fontWeight:700,fontSize:14,cursor:"pointer",flex:1}}>Cancel</button>
                <button onClick={()=>deleteOrder(confirmDelete)} style={{background:C.coral,color:"#fff",border:"none",borderRadius:10,padding:"10px 20px",fontWeight:700,fontSize:14,cursor:"pointer",flex:1}}>Remove</button>
              </div>
            </div>
          </div>
        )}

        {/* ── ADD RECEIPT ── */}
        {tab==="add" && (
          <div style={{animation:"fadeUp 0.35s ease"}}>
            <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"16px":"20px",marginBottom:12}}>
              <div style={{display:"flex",flexDirection:isMobile?"column":"row",gap:isMobile?16:24}}>
                <div style={{flex:1}}>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:12}}>SELECT STORE</div>
                  <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
                    {["Wegmans","Whole Foods","Other"].map(s=>(
                      <button key={s} onClick={()=>setStore(s)} style={{background:store===s?C.lime:"transparent",color:store===s?"#000":C.muted,border:\`1px solid \${store===s?C.lime:C.border}\`,borderRadius:20,padding:"8px 16px",fontWeight:700,fontSize:13,cursor:"pointer"}}>
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
                <div style={{flex:1}}>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:12}}>ORDER DATE</div>
                  <input
                    type="date"
                    value={orderDate}
                    onChange={(e)=>setOrderDate(e.target.value)}
                    style={{background:C.bg,border:\`1px solid \${C.lime}\`,borderRadius:10,color:C.text,padding:"8px 14px",fontSize:14,outline:"none",width:"100%",fontFamily:"inherit",cursor:"pointer"}}
                  />
                  <div style={{fontSize:11,color:C.muted,marginTop:6}}>Overrides date on receipt if found</div>
                </div>
              </div>
            </div>
            <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"16px":"20px"}}>
              <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:16}}>UPLOAD RECEIPT</div>
              <UploadZone onFile={handleFile} onText={handleText} label="Drop or tap to upload receipt" accept="image/*,application/pdf" placeholder="Paste receipt text here..." />
            </div>
          </div>
        )}

        {/* ── ESTIMATE ── */}
        {tab==="estimate" && (
          <div style={{animation:"fadeUp 0.35s ease"}}>
            <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"16px":"20px",marginBottom:12}}>
              <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1,marginBottom:6}}>MEAL PLAN COST ESTIMATOR</div>
              <div style={{fontSize:13,color:C.muted,marginBottom:16}}>Paste your weekly meal plan and get an estimated grocery cost based on your history.</div>
              <UploadZone onFile={()=>{}} onText={handleMealPlan} label="Upload meal plan" accept="image/*,application/pdf" placeholder="e.g. Monday: grilled salmon + asparagus + sweet potato&#10;Tuesday: chicken stir fry with peppers and rice noodles..." />
            </div>
            {estimate&&(
              <div style={{background:C.card,borderRadius:14,border:\`1px solid \${C.border}\`,padding:isMobile?"16px":"20px",animation:"fadeUp 0.35s ease"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16}}>
                  <div style={{fontSize:10,fontWeight:700,color:C.muted,letterSpacing:1}}>ESTIMATED CART</div>
                  <div style={{fontSize:20,fontWeight:800,color:C.lime,fontFamily:"'Space Grotesk',sans-serif"}}>\${estimate.items.reduce((s,i)=>s+i.estimated_price,0).toFixed(2)}</div>
                </div>
                {estimate.store_reasoning&&(
                  <div style={{background:C.bg,borderRadius:10,padding:"10px 12px",marginBottom:14,fontSize:12,color:C.muted,lineHeight:1.6,borderLeft:\`3px solid \${C.sky}\`}}>
                    <strong style={{color:C.sky}}>Recommended: {estimate.recommended_store}</strong> — {estimate.store_reasoning}
                  </div>
                )}
                <div style={{display:"flex",flexDirection:"column",gap:6}}>
                  {estimate.items.map((item,i)=>(
                    <div key={i} style={{display:"flex",alignItems:"center",justifyContent:"space-between",gap:8}}>
                      <div style={{display:"flex",alignItems:"center",gap:6,minWidth:0,flex:1}}>
                        <Pill label={item.category} />
                        <span style={{fontSize:12,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{item.name}</span>
                        {item.from_history&&<span style={{fontSize:10,color:C.sky,background:"#4ECDC422",border:"1px solid #4ECDC4",borderRadius:8,padding:"1px 6px",flexShrink:0}}>history</span>}
                        {item.from_search&&<span style={{fontSize:10,color:C.orange,background:"#FF9F1C22",border:"1px solid #FF9F1C",borderRadius:8,padding:"1px 6px",flexShrink:0}}>web</span>}
                        {item.needs_lookup&&<span style={{fontSize:10,color:C.muted,background:"#88888822",border:"1px solid #888",borderRadius:8,padding:"1px 6px",flexShrink:0}}>est</span>}
                      </div>
                      <span style={{fontSize:13,fontWeight:700,color:C.lime,flexShrink:0}}>\${item.estimated_price.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
  <title>CartIQ</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://unpkg.com/recharts@2.12.0/umd/Recharts.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0F0F1A; overflow-x: hidden; }}
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
    // Make recharts available as module-style imports
    const {{ LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend }} = Recharts;
    const {{ useState, useEffect, useRef }} = React;

    // Stub out window.storage using localStorage
    window.storage = {{
      get: (key) => {{ try {{ const v = localStorage.getItem(key); return Promise.resolve(v ? {{value: v}} : null); }} catch(e) {{ return Promise.resolve(null); }} }},
      set: (key, value) => {{ try {{ localStorage.setItem(key, value); return Promise.resolve({{value}}); }} catch(e) {{ return Promise.resolve(null); }} }},
      delete: (key) => {{ try {{ localStorage.removeItem(key); return Promise.resolve({{deleted: true}}); }} catch(e) {{ return Promise.resolve(null); }} }},
      list: () => Promise.resolve({{keys: []}})
    }};
  </script>
  <script type="text/babel" data-presets="react">
    {JSX_CODE}
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(React.createElement(App));
  </script>
</body>
</html>"""

components.html(html, height=900, scrolling=True)
