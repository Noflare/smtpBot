const puppeteer = require("puppeteer");
const { faker } = require("@faker-js/faker");
const socket = require("socket.io-client")("http://IP_ADRESS:5000");

socket.on("connect", () => {
    console.log("Connected to WebSocket");
});

const repeatCount = 10; // Nombre de fois que le code sera exécuté en boucle

(async () => {
    const receivedLinks = []; // Créer un tableau pour stocker les liens reçus pendant chaque itération

    for (let i = 0; i < repeatCount; i++) {
        const browser = await puppeteer.launch({
            executablePath: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            args: ["--no-sandbox", "--disable-setuid-sandbox"],
            headless: false
        });

        const page = await browser.newPage();
        const link = "YOUR_LINK";
        await page.goto(link);

        await page.evaluate(() => {
            const loginModal = document.getElementById('login-modal');
            if (loginModal) {
                loginModal.classList.add('is-active');
            }
        });

        const randomFirstName = faker.person.firstName();
        const randomLastName = faker.person.lastName();

        await page.waitForSelector('input[name="Entries[full_name]"]');
        await page.type('input[name="Entries[full_name]"]', `${randomFirstName} ${randomLastName}`);

        await page.waitForSelector('input[name="Entries[email]"]');
        await page.type('input[name="Entries[email]"]', randomFirstName + randomLastName + "@besavvy.fr");

        /*await page.waitForSelector('input[name="terms_text"]');
        await page.click('input[name="terms_text"]');*/

        await page.waitForSelector('button[class="button is-primary editable-hover complete-button"]');
        await page.click('button[class="button is-primary editable-hover complete-button"]');

        const urlPromise = new Promise((resolve) => {
            socket.on("link", (data) => {
                receivedLinks.push(data); // Ajouter le lien reçu au tableau
                resolve(data);
            });
        });

        const url = await urlPromise;

        const page2 = await browser.newPage();
        await page2.goto(url);

        await browser.close();

        console.log(`Iteration ${i + 1} finished. Waiting for next iteration...`);
        await new Promise(resolve => setTimeout(resolve, 3000)); // Pause de 5 secondes

        receivedLinks.length = 0; // Vider le tableau des liens reçus après chaque itération
    }
})();
