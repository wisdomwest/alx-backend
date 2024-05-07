import { promisify } from 'util';
import { createClient } from 'redis';
import express from 'express';

const client = createClient();

client.on('error', (err) => {
  console.log(`Error: ${err}`);
});

const listProducts = [
  {
    Id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4
  },
  {
    Id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    Id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    Id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5
  }
];

function parse(product) {
  const modified = {};
  modified.itemId = product.Id;
  modified.itemName = product.name;
  modified.price = product.price;
  modified.initialAvailableQuantity = product.stock;
  return modified;
}

function getAllItems() {
  return listProducts.map(parse);
}

function getItemById(id) {
  for (const product of listProducts) {
    if (product.Id === id) {
      return parse(product);
    }
  }
  return {}
}

function reserveStockById(itemId, stock) {
  const SET = promisify(client.SET).bind(client);
  return SET(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const GET = promisify(client.GET).bind(client);
  const reservedStock = await GET(`item.${itemId}`);
  if (reservedStock === null) {
    return 0;
  }
  return reservedStock;
}

const app = express();

app.get('/list_products', (req, res) => {
  res.json(getAllItems());
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (Object.keys(item).length === 0) {
    return res.json({ status: 'Product not found' });
  }
  const reservedStock = await getCurrentReservedStockById(itemId);
  item.currentQuantity = item.initialAvailableQuantity - reservedStock;
  return res.json(item);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (Object.keys(item).length === 0) {
    return res.json({ status: 'Product not found' });
  }
  const reservedStock = await getCurrentReservedStockById(itemId);
  if (reservedStock >= item.initialAvailableQuantity) {
    return res.json({ status: 'Not enough stock available', itemId });
  }
  await reserveStockById(itemId, reservedStock + 1);
  return res.json({ status: 'Reservation confirmed', itemId });
});


app.listen(1245, async () => {
  console.log('API listening on port 1245');
});
