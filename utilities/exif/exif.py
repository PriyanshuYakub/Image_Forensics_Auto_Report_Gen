import exiftool

class ExifTool:
    def __init__(self, image_path):
        self.image_path = image_path
        self.metadata = None
        self.extract_metadata()

    def extract_metadata(self):
        with exiftool.ExifTool() as et:
            self.metadata = et.get_metadata(self.image_path)

    def print_metadata(self):
        if self.metadata is not None:
            print("Metadata Found!!")
            # for tag, value in self.metadata.items():
            #     print(f"{tag}: {value}")
            # print(self.metadata)
            
        else:
            print("No metadata found.")

# Test
# if __name__ == "__main__":
#     img_path = '../testfiles/img1.jpg'
#     tool = ExifTool(img_path)
#     tool.print_metadata()
