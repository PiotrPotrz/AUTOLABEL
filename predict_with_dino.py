import torch
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from data import DataLoader
import pandas as pd
import time
import warnings


class PredictWithDino:
    def __init__(self):
        model_id = "IDEA-Research/grounding-dino-tiny"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if self.device != torch.device("cuda"):
            warnings.warn("WARNING: Cuda not available.")
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(self.device)
        self.columns = ["name", "label", "score", "x_min", "y_min", "x_max", "y_max"]

    def __make_df(self, data):
        return pd.DataFrame(data, columns=self.columns)

    def predict_and_save(self, data_loader: DataLoader, box_threshold, text_threshold, text):
        data = []
        print("LOADING DATA")
        image_names, image_array = data_loader.load_folder()
        height = data_loader.height
        width = data_loader.width
        channels = data_loader.channels

        print("PROCESSING DATA")
        start_time = time.time()
        for i, image in enumerate(image_array):
            vid_name = image_names[i]
            inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)

            results_test = self.processor.post_process_grounded_object_detection(
                outputs,
                inputs.input_ids,
                box_threshold=box_threshold,
                text_threshold=text_threshold,
                target_sizes=[(height, width)]
            )
            results_test = results_test[0]
            if len(results_test["scores"]) != 0:
                for j in range(len(results_test["scores"])):
                    print(vid_name)
                    x_min, y_min, x_max, y_max = map(int, results_test["boxes"].cpu().numpy()[j])
                    label = results_test["labels"][j].replace("[SEP]", "").replace(".", "").strip()
                    data.append([vid_name, label, results_test["scores"].cpu().numpy()[j], x_min, y_min, x_max, y_max])
        end_time = time.time()
        df = self.__make_df(data)
        print(end_time - start_time)
        return df

    def preview(self, loader, text):
        return