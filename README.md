# ✨ Groq-Powered Alpaca Dataset Transformation and Finetuning for Enhanced HTML Generation 🦙

This project focuses on enhancing the Alpaca dataset for generating HTML outputs using the Groq API and applying Unsloth finetuning techniques. The enhanced dataset is then used to finetune a Llama 3.1 7b model, resulting in improved performance for HTML generation tasks, including notably, correctly answering challenging questions like counting specific letters within words (e.g., the number of "r"s in "strawberry"). The finetuned models are then pushed to Hugging Face Hub with different weight configurations.  You can find the model here: [Vinitrajputt/COT-html-lamma](https://huggingface.co/Vinitrajputt/COT-html-lamma)

## 🚀 Project Overview

This project involves several key steps:

1. **Alpaca Dataset Acquisition and Conversion:** The original Alpaca dataset is fetched and converted into a JSON format for easy processing.
2. **Groq API Transformation (using Llama 3.1 7b):** The Groq API is leveraged, specifically using the Llama 3.1 7b model, to transform the Alpaca dataset into a new format tailored for HTML generation. This involves prompting the model to think step-by-step using the Chain-of-Thought (CoT) reasoning approach and then generate corresponding HTML output. The prompt also encourages beautiful and interactive UI design using only internal CSS and JS.
3. **Dataset Chunking and Merging:** The transformed dataset is split into six chunks for manageable processing and then merged back together into a single comprehensive dataset.
4. **Unsloth Finetuning:** The merged dataset is then used to finetune the Llama 3.1 7b model using the Unsloth technique. This process optimizes the model's ability to generate high-quality HTML based on user instructions.
5. **Hugging Face Model Deployment:** Finally, the finetuned model is uploaded to Hugging Face Hub ([https://huggingface.co/Vinitrajputt/COT-html-lamma](https://huggingface.co/Vinitrajputt/COT-html-lamma)) with different weight configurations (BF16, F16, quantized versions Q4_K_M, Q5_K_M, and Q8_0), allowing for easy access and experimentation.  The repository also includes essential files like `README.md`, `adapter_config.json`, `adapter_model.safetensors`, `config.json`, `special_tokens_map.json`, `tokenizer.json`, and `tokenizer_config.json`.

## 🌟 Key Achievement: Solving the "Strawberry" Challenge

This finetuned model demonstrates a significant improvement in logical reasoning by accurately answering the question "How many 'r's are in the word 'strawberry'?" This is achieved by prompting the model with a specific CoT structure that encourages it to check for the presence of the word before counting the letters:


```html
<[COT]> 
  First check if all the letters of "strawberry" is there in the sentence then count the number of r's.
   If yes, then count them and return result as HTML. 
  else return error message 
</[COT]>
<[HTML]>
  <div id="result"> 
    <!-- Add javascript here to generate a HTML response -->
  </div>
  <script>
     // Write javascript code here
     var text = "strawberry";
     if (text.toLowerCase().includes("strawberry"))
         document.getElementById("result").innerHTML = `There are ${text.match(/r/g).length} R in the word Strawberry`; // Corrected string interpolation
     else{
         document.getElementById("result").innerHTML = "Sorry we can't find any R in the word.";
     }
  </script>
</[HTML]>
```

This approach guides the model to perform the necessary check, leading to the correct HTML output with the embedded JavaScript dynamically calculating and displaying the count of "r"s. This demonstrates an enhanced ability to handle complex logic within HTML generation tasks.

## 🛠️ Technologies Used

* **Alpaca Dataset:** [https://crfm.stanford.edu/2023/03/13/alpaca.html](https://crfm.stanford.edu/2023/03/13/alpaca.html)
* **Groq API:** [https://groq.com/docs/](https://groq.com/docs/)
* **Llama 3.1 7b:** The specific language model used for transformation and finetuning.
* **Python:** For data processing and API interaction.
* **JSON:** For data storage and manipulation.
* **Unsloth:** For efficient finetuning of the language model.
* **Hugging Face Hub:** For model hosting and sharing.
* **tqdm:** For progress bar visualization during processing.
* **JavaScript:** Used within the generated HTML for dynamic content.





## 📂 Dataset Format

The original Alpaca dataset format:

```json
[
  {
    "instruction": "Give three tips for staying healthy.",
    "input": "",
    "output": "1.Eat a balanced diet and make sure to include plenty of fruits and vegetables. \n2. Exercise regularly to keep your body active and strong. \n3. Get enough sleep and maintain a consistent sleep schedule."
  },
  ...
]
```

The transformed dataset format after processing with the Groq API:

```json
[
    {
        "instruction": "Give three tips for staying healthy.",
        "input": "",
        "output": "1.Eat a balanced diet and make sure to include plenty of fruits and vegetables. \n2. Exercise regularly to keep your body active and strong. \n3. Get enough sleep and maintain a consistent sleep schedule.",
        "response": "<[COT]> ... <[/COT]> \n\n<[HTML]> ... <[/HTML]>"
    },
    ...
]
```

The key addition is the `response` field, which contains both the Chain-of-Thought (CoT) reasoning within `<[COT]>` tags and the generated HTML within `<[HTML]>` tags.


## 💻 Code Example (Dataset Creation)

The provided code demonstrates the process of fetching the Alpaca dataset, transforming it using the Groq API, and saving the results to a JSON file.  Key features include API key rotation for handling rate limits and real-time JSON updates to prevent data loss in case of interruptions.  See the `dataset_generation.py` file (or the code block in your original prompt) for the full implementation.

## ✨ Key Improvements and Considerations

* **API Key Rotation:**  The code includes a mechanism to rotate through multiple Groq API keys, mitigating rate limit issues and ensuring continuous processing.
* **Real-time JSON Updates:**  The dataset is updated after each successful API call, minimizing the risk of data loss.
* **Error Handling:** The script includes basic error handling and fallback mechanisms to handle API issues.
* **Rate Limiting:** Explicit delays are implemented to respect Groq API rate limits.

## 👣 Future Work

* **More Robust Error Handling:**  Implement more sophisticated error handling to gracefully handle various potential issues.
* **Advanced Prompt Engineering:** Experiment with different prompt structures to further improve the quality and relevance of generated HTML.
* **Automated Evaluation Metrics:** Develop automated metrics to evaluate the quality and usability of the generated HTML.
* **Model Optimization:**  Explore different model architectures and finetuning techniques to optimize performance for specific HTML generation tasks.


## 🤝 Contributing

Contributions to this project are welcome!  Feel free to open issues or submit pull requests.
