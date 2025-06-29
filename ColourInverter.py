import pygame

class App:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1,1))

    # Checks for end command
    def check_for_end_command(self,prompt):
        if prompt.lower().replace(" ","") == "end":
            print("Ended Session")
            return False
        
        return True

    def invert(self, path):
        # Load image
        image = pygame.image.load(fr"{path.removeprefix('"').removesuffix('"')}").convert()

        # Pixel array
        pixel_array = pygame.surfarray.array3d(image)

        # Acquire width and height correctly
        width, height = pixel_array.shape[:2]

        # Iterate through the pixels
        for x in range(width):
            for y in range(height):
                # Acquire rgb values
                r, g, b = pixel_array[x, y]

                # Invert
                pixel_array[x, y] = (255 - r, 255 - g, 255 - b)

        # Convert array back into surface
        updated_surface = pygame.surfarray.make_surface(pixel_array)

        return updated_surface

    # Main code
    def run(self):
        running = True
        while running:

            try:
                # Check for inversion commands
                path_prompt = input("Please state the absolute/workingdir path of the file: ").strip()
                running = self.check_for_end_command(path_prompt)

                if running:
                    save_file_name = input("Please state your save file path (absolute otherwise stored in the inversion folder): ").strip()

                    inverted_image = self.invert(path_prompt)
                    pygame.image.save(inverted_image,save_file_name)
                    print(f"File saved as {save_file_name}")

        
            except Exception as e:
                print(f"Error occured: {e}. Aborting generation...")

        pygame.quit()

app = App()

if __name__ == "__main__":
    app.run()