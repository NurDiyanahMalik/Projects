import OpenAI from 'openai';
import readlineSync from 'readline-sync';



OPENAI_API_KEY = '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'
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY 
});

async function main() {
    const chatHistory = [];
    while (true) {
        const userInput = readlineSync.question('Question: ');
        try { 
            const messages = chatHistory.map(([role, content]) => ({role,content}));

            messages.push({role:'user', content: userInput });
        
            const chatCompletion = await openai.chat.completions.create({
                model: "gpt-3.5-turbo",
                messages: messages,
            });
            const completionText = chatCompletion.choices[0].message;

            chatHistory.push(['user', userInput]);
            chatHistory.push(['assistant', completionText]);

            if (userInput.toLowerCase() === 'done') {
                return;
            }
        } catch (error) {
                console.error(error);
        }
        
    }
}

main();
