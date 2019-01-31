<?php

namespace Buttbot\Plugins;

use Phergie\Irc\Bot\React\AbstractPlugin;
use Phergie\Irc\Bot\React\EventQueueInterface as Queue;
use Phergie\Irc\Plugin\React\Command\CommandEvent as Event;
use Zttp\Zttp;

class Weather extends AbstractPlugin {

    private $apiKey = '';

    public function __construct(array $config = [])
    {
        if (isset($config['apiKey'])) {
            $this->apiKey = $config['apiKey'];
        }
    }

    public function getSubscribedEvents()
    {
        return ['command.weather' => 'handleCommand'];
    }

    public function handleCommand(Event $event, Queue $queue)
    {
        $location = $event->getCustomParams();
        if (count($location) > 0) {
            $response = Zttp::get('http://api.apixu.com/v1/current.json', ['key' => $this->apiKey, 'q' => implode(' ', $location)]);
            if ($response->status() !== 200) {
                $this->sendIrcResponse($event, $queue, ['An error occurred when retrieving weather data']);
            }
            $data = $response->json();
            $weatherData = sprintf('"%s" and the temperature is %s°C (%s°F)', $data["current"]["condition"]["text"], $data["current"]["temp_c"], $data["current"]["temp_f"]);
            $locationData = sprintf("%s, %s, %s", $data["location"]["name"], $data["location"]["region"], $data["location"]["country"]);

            $this->sendIrcResponse($event, $queue, [sprintf("The weather in %s is %s.", $locationData, $weatherData)]);

        }
    }

    protected function sendIrcResponse(Event $event, Queue $queue, array $ircResponse)
    {
        foreach ($ircResponse as $ircResponseLine) {
            $this->sendIrcResponseLine($event, $queue, $ircResponseLine);
        }
    }

    protected function sendIrcResponseLine(Event $event, Queue $queue, $ircResponseLine)
    {
        $queue->ircPrivmsg($event->getSource(), $ircResponseLine);
    }
}
