import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useRef, useState } from 'react';
import { Alert, Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import{ router, useFocusEffect } from 'expo-router';
import React from 'react';
import { Image } from 'expo-image';
import axios from 'axios';
import { Stack } from "expo-router";
import { API_URL, API_TIMEOUT } from '../config/config';

function CameraScreen(){
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [isPreview, setIsPreview] = useState(false);
  const [photoUri, setPhotoUri] = useState<string | null>(null);
  const cameraRef = useRef<any>(null);
  const [cameraKey, setCameraKey] = useState<number>(0);
  const [isLoading, setIsLoading] = useState(false);

  useFocusEffect(
    React.useCallback(() => {
      if(cameraRef.current){
        cameraRef.current.resumePreview();
        setIsPreview(false);
      }
      setPhotoUri(null);
    }, [isPreview])
  );

  if (!permission) {
    // Camera permissions are still loading.
    return <View />;
  }

  if (!permission.granted) {
    // Camera permissions are not granted yet.
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="grant permission" />
      </View>
    );
  }

  /* Take a Picture Function */
  const takePicture = async () => {
    if (cameraRef.current) {
      const options = { quality: 0.5, base64: true };
      const data = await cameraRef.current.takePictureAsync(options);
      const source = data.uri;
      setPhotoUri(source);
      if (source) {
        await cameraRef.current.pausePreview();
        setIsPreview(true);
        console.log("picture source", source);
      }
    }
  };

  /* Reake a Picture Function */
  const retakePicture = () => {
    setPhotoUri(null);
    setIsPreview(false);
    setCameraKey(prev => prev + 1);
  };

  const toResultPage = async () => {
    if (photoUri){
      setIsLoading(true);
      router.push("/LoadingScreen");

      const formData = new FormData();
      const filename = photoUri.split('/').pop();

      formData.append('file', {
          uri: photoUri,
          type: 'image/jpeg',
          name: filename,
        } as any);

      try {
        console.log('Sending request to backend...');

        const response = await axios.post(`${API_URL}/predict`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          timeout: API_TIMEOUT,
        });

        const result = response.data;
        console.log('=== Upload Successful ===');
        console.log('Prediction result:', result);

        setIsLoading(false);

        router.replace({
          pathname: '/ResultPage',
          params: { 
            photoUri,
            prediction: result.predicted_class,
          },
        });
      } catch (error) {
        setIsLoading(false);

        if (axios.isAxiosError(error)) {
          console.error('Upload error details:', {
            message: error.message,
            response: error.response?.data,
            status: error.response?.status,
          });
        } else {
          console.log("Other error:", error);
        }

        Alert.alert(
          "Prediction Failed",
          "Unknown error occurred",
        );
        
        router.push('/')
      }
    }
  };

  return (
    <View style={styles.container}>

      {photoUri ? (
        <Image source={{ uri: photoUri }} style={{height: 400, width: 400}} />
      ) : (
        <View style={styles.cameraContainer}>
          <Text style={styles.title}>Please Take Your Plant's Picture</Text>
          <CameraView key={cameraKey} ref={cameraRef} style={styles.camera} facing={facing} />
        </View>
      )}

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} >
          <Text style={styles.text} onPress={takePicture} disabled={isLoading || isPreview}>Take a Picture</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} >
            <Text style={styles.text} onPress={retakePicture}>try again</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={toResultPage} disabled={isLoading}>
            <Text style={styles.text}>Submit !</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default function Home() {
  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <CameraScreen />
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 50,
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  cameraContainer: {
    width: '80%',
    aspectRatio: 3 / 4,
    overflow: 'hidden',
    borderRadius: 10,
    marginBottom: 30,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    marginTop: 20,
    flexDirection: 'row',
    paddingHorizontal: 64,
  },
  button: {
    backgroundColor: '#008000',
    paddingHorizontal: 25,
    paddingVertical: 15,
    borderRadius: 10,
    paddingLeft: 20,
    paddingRight: 20,
  },
  text: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
});
