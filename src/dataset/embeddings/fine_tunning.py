from transformers import AutoTokenizer, AutoModelForMaskedLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from datasets import load_dataset

# Nombre del modelo base
model_name = "dccuchile/bert-base-spanish-wwm-cased"

# Cargar modelo y tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForMaskedLM.from_pretrained(model_name)

# Cargar tu corpus (ejemplo: un archivo de texto plano)
# Suponiendo que tienes 'corpus_medico.txt'
dataset = load_dataset('text', data_files={'train': 'corpus_medico.txt'})

# Tokenizar el dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], return_special_tokens_mask=True, truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Data collator para crear dinámicamente las máscaras
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

# Configurar el Trainer
training_args = TrainingArguments(
    output_dir="./beto-medico-finetuned",
    overwrite_output_dir=True,
    num_train_epochs=2,
    per_device_train_batch_size=8,
    save_steps=500,
    save_total_limit=2,
    prediction_loss_only=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator
)

# Fine-tuning
trainer.train()

# Guardar modelo
trainer.save_model("./beto-medico-finetuned")
