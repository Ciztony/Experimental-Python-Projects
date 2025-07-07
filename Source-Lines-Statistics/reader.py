from os.path import exists,isdir,join,basename
from os import walk
import sys


class SourceLinesReader:
    # Ends the session
    def checkForEndCommand(self,prompt):
        if prompt.lower().replace(" ","") == "end":
            print("Ended Session.")
            sys.exit()

    # Get types of file for extraction
    def checkForFileExtractionTypes(self):
        fileExtractionInput = input("Please input the types of files you want (e.g txt(//),py(#)). Note the brackets store the comments, leave blank if you want them included: ")
        self.checkForEndCommand(fileExtractionInput)
        tokenizedFileTypes = [fileType.strip() for fileType in list(fileExtractionInput.split(","))] # Split the user input into several file types for parsing
        return tokenizedFileTypes
    
    # Get formatting errors in file
    def hasIncorrectParentheses(self,string,errorType,parentheses):
        p1,p2 = parentheses

        if (p1 in string) != (p2 in string): # Warn user that the input for file type was formatted incorrectly, e.g "py(#"
            print(f"WARNING! {errorType} {string} will not be considered due to bad formatting!")
            return True
        return False

    
    # Parse comment string into several types
    def parseIntoDifferentCommentTypes(self,commentStr,fileType):
        hasIncorrectParentheses = self.hasIncorrectParentheses
        commentTypes = []
        tokenizedCommentTypes = [comment.strip().replace(" ","") for comment in commentStr.split("^")]
        for comment in tokenizedCommentTypes:
            # Checks to ensure that both parentheses are included in the comment
            if hasIncorrectParentheses(comment,f"Comment type of fileType {fileType}",["[","]"]):
                continue

            if "[" not in comment and "]" not in comment:
                commentTypes.append(comment)
                continue
            
            if comment[0] == "[" and comment[-1] == "]":
                commentTypes.append(comment.strip("[]").split("|")) # Strip and return as string
        return commentTypes
            
    
    # Parse user input for file types like py(#) into separate tokens py, # to allow exclusion of commentss
    def processFileTypeInput(self,tokenizedFileTypes):
        hasIncorrectParentheses = self.hasIncorrectParentheses
        fileDict = {}
        isCheckingForComment = False
        for fileType in tokenizedFileTypes:

            # Checks to ensure that both parentheses are included in the command
            if hasIncorrectParentheses(fileType,"Filetype",["(",")"]):
                continue

            fileStr = ""
            commentStr = ""
            for char in fileType: 
                if char == ")":
                    isCheckingForComment = False

                if isCheckingForComment: # If in comment, add to comment
                    commentStr += char
                else:
                    fileStr += char

                if char == "(":
                    isCheckingForComment = True
        
            cleanedFileStr = fileStr.removesuffix("()").strip()
            fileDict[cleanedFileStr] = self.parseIntoDifferentCommentTypes(commentStr.strip(),fileType) # Remove extra part due to incorrect conditionals 
            self.types.setdefault(cleanedFileStr,0)
            # (Note pls don't change this idk how to explain)
        return fileDict
    

    def checkLineForSameDelimiter(self, stripped, delimiter):
        count = stripped.count(delimiter)

        if self.isInMultiline:
          
            if count % 2 == 1:
                self.isInMultiline = False
            return True
        else:
            if count == 0:
                return False
            elif count % 2 == 1:
                self.isInMultiline = True
                return True
            else:
                
                return True

    def checkLineForDifferentDelimiter(self, stripped, comment):
        startDelim, endDelim = comment

        if self.isInMultiline:
            if endDelim in stripped:
                self.isInMultiline = False
                return True
            return True  
        else:
            if startDelim in stripped:
                if endDelim in stripped and stripped.find(startDelim) < stripped.find(endDelim):
                
                    return True
                else:
                    self.isInMultiline = True
                    return True
        return False  # Not a comment

    def checkAtLineForCommentTypes(self,stripped,commentTypes):
        for comment in commentTypes:
            if isinstance(comment,list):
                if comment[0] == comment[1]:
                    return self.checkLineForSameDelimiter(stripped,comment[0])
                else:
                    return self.checkLineForDifferentDelimiter(stripped,comment)
            else:
                if stripped.startswith(comment):
                    return True
        return False # Only return false if none match
    
    def returnLineNumber(self, filePath, commentTypes,fileExtension=None):
        count = 0
        checkAtLineForCommentTypes = self.checkAtLineForCommentTypes
        self.isInMultiline = False
        with open(filePath, "r", encoding="utf-8") as f:
            if commentTypes != ['']:
                for line in f:
                    stripped = line.strip()               
                    check = checkAtLineForCommentTypes(stripped,commentTypes)
                    if stripped and not check: # Ensures the line is neither blank nor starts with a comment
                        count += 1
                        if fileExtension:
                            self.types[fileExtension] += 1
            else:     
                for line in f:
                    if line.strip(): # Ensures the line is neither blank nor starts with a comment
                        count += 1 
                        if fileExtension:
                            self.types[fileExtension] += 1


        return count

    def walkThroughFilesInDir(self,path,fileTypes):
        numberOfLines = 0
        getLineNumber = self.returnLineNumber
        for root, _, files in walk(path):
            for filename in files:
                matchedSuffix = next((s for s in fileTypes.keys() if filename.endswith(s.lower())), None) # Acquire the first filetype extension that matches the file 
                if matchedSuffix:
                    commentType = fileTypes[matchedSuffix] # Get comment type if specified
                    numberOfLines += getLineNumber(join(root,filename),commentType,matchedSuffix) # Get number of lines in file
        return numberOfLines
    
        
    def askForFilePath(self):
        inputPath = input("Please input the folder path or file path to the source file (Can be relative or absolute path): ")
        path = inputPath.strip().strip('"\'') # Clears unwanted quotes when absolute path is inputted
        print(f"Filepath: {path}")
        self.checkForEndCommand(path)
        return path
    
    def printLines(self):
        print("-------")
        for extension,lines in self.types.items():
            print(f"{extension}: {lines}")
    
    def run(self):
        self.types = {}
        while not exists(path := self.askForFilePath()): # Ask for file/folder path
            print(f"File path: {path} does not exist")

        if isdir(path):
            tokenizedFileTypes = self.checkForFileExtractionTypes()
            fileTypes = self.processFileTypeInput(tokenizedFileTypes)
            print("Lines:",self.walkThroughFilesInDir(path,fileTypes))
            self.printLines()
        else:
            commentTypeInput = input("Please specify the comments if you want to exclude, e.g #: ").strip()
            commentTypes = self.parseIntoDifferentCommentTypes(commentTypeInput,basename(path)[1]) # Get filetype
            print("Lines:",self.returnLineNumber(path,commentTypes))

if __name__ == "__main__":
    sourceReader = SourceLinesReader()
    sourceReader.run()

    
    
    